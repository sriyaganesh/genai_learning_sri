import streamlit as st
import os
import tempfile
import hashlib
import sys
import certifi
import atexit

from dotenv import load_dotenv
from neo4j import GraphDatabase

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

from duckduckgo_search import DDGS

# ==============================
# 🔐 ENV + SSL FIX
# ==============================
load_dotenv()

if sys.platform == "win32":
    os.environ["SSL_CERT_FILE"] = certifi.where()

DOCS_PATH = "docs"

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USERNAME")
NEO4J_PASS = os.getenv("NEO4J_PASSWORD")

# ==============================
# 🔌 NEO4J DRIVER
# ==============================
@st.cache_resource
def get_driver():
    return GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASS)
    )

driver = get_driver()

@atexit.register
def close_driver():
    driver.close()

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
# 🧠 VECTOR STORE (FAISS)
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
        data = [{"text": doc.page_content[:1500]} for doc in docs]

        session.run("""
            UNWIND $rows AS row
            CREATE (d:Document {text: row.text})
        """, {"rows": data})


# ==============================
# 🔍 GRAPH SEARCH (IMPROVED)
# ==============================
def query_neo4j(query):
    stopwords = {"what", "is", "are", "the", "of", "in", "on", "a", "an"}

    keywords = [
        word for word in query.lower().split()
        if word not in stopwords and len(word) > 2
    ]

    cypher = """
    MATCH (d:Document)
    WHERE ANY(word IN $words WHERE toLower(d.text) CONTAINS word)
    RETURN d.text LIMIT 8
    """

    with driver.session() as session:
        result = session.run(cypher, {"words": keywords})
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
    retriever = db.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(query)

    context = "\n".join([d.page_content for d in docs])

    llm = ChatOpenAI(model_name="gpt-4", temperature=0)

    return llm.invoke(f"""
    Answer ONLY using context.
    If not found return NOT_FOUND.

    Context:
    {context}

    Question:
    {query}
    """).content


# ==============================
# 🤖 GRAPH RAG
# ==============================
def graph_rag(query):
    graph_data = query_neo4j(query)

    llm = ChatOpenAI(model_name="gpt-4", temperature=0)

    return llm.invoke(f"""
    Answer using graph data below.

    Even partial info is fine.

    If nothing relevant return NOT_FOUND.

    Data:
    {graph_data}

    Question:
    {query}
    """).content


# ==============================
# 🧠 ANSWER COMPARISON
# ==============================
def compare_answers(query, faiss_ans, graph_ans):
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)

    decision = llm.invoke(f"""
    Compare two answers and pick the best.

    Question:
    {query}

    Answer 1 (FAISS):
    {faiss_ans}

    Answer 2 (GRAPH):
    {graph_ans}

    Rules:
    - Choose more accurate & complete
    - Prefer factual grounding
    - If both bad return NONE

    Output ONLY:
    ANSWER_1 or ANSWER_2 or NONE
    """).content.strip()

    if "ANSWER_1" in decision:
        return faiss_ans
    elif "ANSWER_2" in decision:
        return graph_ans
    else:
        return None


# ==============================
# 🚀 HYBRID RAG (COMPARISON)
# ==============================
def hybrid_rag(query, db):
    faiss_ans = faiss_rag(query, db)
    graph_ans = graph_rag(query)

    final = compare_answers(query, faiss_ans, graph_ans)

    fallback = False

    if final is None or "NOT_FOUND" in str(final):
        fallback = True
        web_data = web_search(query)

        llm = ChatOpenAI(model_name="gpt-4", temperature=0)

        final = llm.invoke(f"""
        Use web data to answer:

        {web_data}

        Question: {query}
        """).content

    return final, faiss_ans, graph_ans, fallback


# ==============================
# 🎨 STREAMLIT UI
# ==============================
st.set_page_config(page_title="Hybrid RAG Comparison", layout="wide")

st.title("🚀 Hybrid RAG (FAISS vs Graph Comparison)")

if st.button("🔄 Rebuild Index"):
    st.cache_resource.clear()
    st.success("Cache cleared!")

documents, file_names = [], []

docs, names = load_docs_from_folder()
documents.extend(docs)
file_names.extend(names)

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    up_docs, up_name = load_uploaded_file(uploaded_file)
    documents.extend(up_docs)
    file_names.append(up_name)

if not documents:
    st.warning("Upload documents!")
    st.stop()

st.write("📂 Files:", file_names)

cache_key = generate_cache_key(file_names)
db, split_docs = build_vectorstore(cache_key, documents)

if st.button("🧠 Build Knowledge Graph"):
    build_knowledge_graph(split_docs)
    st.success("Graph built!")

query = st.text_input("Ask a question")

if st.button("Submit"):
    with st.spinner("Thinking..."):
        final, faiss_ans, graph_ans, fallback = hybrid_rag(query, db)

    st.subheader("✅ Final Answer")
    st.write(final)

    st.divider()

    st.subheader("🔍 FAISS Answer")
    st.write(faiss_ans)

    st.subheader("🕸️ Graph Answer")
    st.write(graph_ans)

    st.subheader("🌐 Fallback Used")
    st.write("Yes" if fallback else "No")

    