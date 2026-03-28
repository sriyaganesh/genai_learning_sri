import streamlit as st
import os
import tempfile
import hashlib

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

from duckduckgo_search import DDGS
from dotenv import load_dotenv

from neo4j import GraphDatabase

load_dotenv()

DOCS_PATH = "docs"

# ==============================
# 🔗 NEO4J CONFIG
# ==============================
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USERNAME")
NEO4J_PASS = os.getenv("NEO4J_PASSWORD")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))


# ==============================
# 📄 LOAD DOCUMENTS
# ==============================
def load_docs_from_folder():
    documents, file_names = [], []

    if not os.path.exists(DOCS_PATH):
        return documents, file_names

    for file in os.listdir(DOCS_PATH):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DOCS_PATH, file))
            docs = loader.load()

            for d in docs:
                d.metadata["source"] = file

            documents.extend(docs)
            file_names.append(file)

    return documents, file_names


def load_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    docs = loader.load()

    for d in docs:
        d.metadata["source"] = uploaded_file.name

    return docs, uploaded_file.name


# ==============================
# 🔑 CACHE KEY
# ==============================
def generate_cache_key(file_names):
    return hashlib.md5("_".join(sorted(file_names)).encode()).hexdigest()


# ==============================
# 🧠 VECTOR DB
# ==============================
@st.cache_resource
def build_vectorstore(cache_key, documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)

    return db, docs


# ==============================
# 🕸️ BUILD KNOWLEDGE GRAPH
# ==============================
def build_knowledge_graph(docs):
    with driver.session() as session:
        #session.run("MATCH (n) DETACH DELETE n")

        for doc in docs:
            text = doc.page_content[:500]

            query = """
            CREATE (d:Document {text: $text})
            """
            session.run(query, text=text)


# ==============================
# 🔍 GRAPH SEARCH
# ==============================
def query_neo4j(query):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (d:Document)
            WHERE d.text CONTAINS $query
            RETURN d.text LIMIT 3
            """,
            query=query
        )

        return "\n".join([r["d.text"] for r in result])


# ==============================
# 🌐 WEB SEARCH
# ==============================
def web_search(query):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=3):
            results.append(r["body"])
    return "\n".join(results)


# ==============================
# 🤖 FAISS RAG
# ==============================
def faiss_rag(query, db):
    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)

    context = "\n".join([d.page_content for d in docs])

    llm = ChatOpenAI(model_name="gpt-4", temperature=0)

    prompt = f"""
    Answer ONLY from context.
    If not found return NOT_FOUND.

    Context:
    {context}

    Question:
    {query}
    """

    response = llm.invoke(prompt)
    return response.content


# ==============================
# 🤖 GRAPH RAG
# ==============================
def graph_rag(query):
    graph_data = query_neo4j(query)

    llm = ChatOpenAI(model_name="gpt-4", temperature=0)

    prompt = f"""
    Answer ONLY from this knowledge graph data.
    If not found return NOT_FOUND.

    Data:
    {graph_data}

    Question:
    {query}
    """

    response = llm.invoke(prompt)
    return response.content


# ==============================
# 🧠 ANSWER EVALUATION
# ==============================
def evaluate_answers(query, ans1, ans2):
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)

    prompt = f"""
    Question: {query}

    Answer 1:
    {ans1}

    Answer 2:
    {ans2}

    Choose best answer.
    If both bad return NONE.

    Return ONLY:
    ANSWER_1 or ANSWER_2 or NONE
    """

    decision = llm.invoke(prompt).content.strip()

    if "ANSWER_1" in decision:
        return ans1
    elif "ANSWER_2" in decision:
        return ans2
    else:
        return None


# ==============================
# 🚀 MAIN RAG PIPELINE
# ==============================
def hybrid_rag(query, db):
    faiss_answer = faiss_rag(query, db)
    graph_answer = graph_rag(query)

    final_answer = evaluate_answers(query, faiss_answer, graph_answer)

    fallback = False

    if final_answer is None or "NOT_FOUND" in str(final_answer):
        fallback = True
        web_data = web_search(query)

        llm = ChatOpenAI(model_name="gpt-4", temperature=0)

        final_answer = llm.invoke(f"""
        Data not found in documents.

        Use web data:
        {web_data}

        Question: {query}
        """).content

    return final_answer, faiss_answer, graph_answer, fallback


# ==============================
# 🎨 STREAMLIT UI
# ==============================
st.set_page_config(page_title="Hybrid RAG + KG Chatbot", layout="wide")

st.title("🚀 Hybrid RAG + Knowledge Graph Chatbot")

if st.button("🔄 Rebuild Index"):
    st.cache_resource.clear()
    st.success("Cache Cleared!")

documents, file_names = [], []

docs, names = load_docs_from_folder()
documents.extend(docs)
file_names.extend(names)

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    up_docs, up_name = load_uploaded_file(uploaded_file)
    documents.extend(up_docs)
    file_names.append(up_name)

if len(documents) == 0:
    st.warning("Upload documents!")
    st.stop()

st.write("📂 Files:", file_names)

cache_key = generate_cache_key(file_names)
db, split_docs = build_vectorstore(cache_key, documents)

# Build KG once
if st.button("🧠 Build Knowledge Graph"):
    build_knowledge_graph(split_docs)
    st.success("Knowledge Graph Built!")

query = st.text_input("Ask a question")

if st.button("Submit"):
    with st.spinner("Processing..."):
        final, faiss_ans, graph_ans, fallback = hybrid_rag(query, db)

    st.subheader("🤖 Final Answer")
    st.write(final)

    st.divider()

    st.subheader("🔍 FAISS Answer")
    st.write(faiss_ans)

    st.subheader("🕸️ Graph Answer")
    st.write(graph_ans)

    st.subheader("🌐 Fallback Used")
    st.write("Yes" if fallback else "No")