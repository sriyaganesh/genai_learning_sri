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

load_dotenv()

DOCS_PATH = "docs"


# ==============================
# 📄 LOAD FILES FROM docs/
# ==============================
def load_docs_from_folder():
    documents = []
    file_names = []

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


# ==============================
# 📄 LOAD UPLOADED FILE
# ==============================
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
# 🔑 CREATE CACHE KEY
# ==============================
def generate_cache_key(file_names):
    key_string = "_".join(sorted(file_names))
    return hashlib.md5(key_string.encode()).hexdigest()


# ==============================
# 🧠 CREATE VECTOR DB (CACHED)
# ==============================
@st.cache_resource
def build_vectorstore(cache_key, documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)

    return db, len(docs)


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
# 🤖 RAG RESPONSE
# ==============================
def get_rag_response(query, db):
    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)

    context = "\n".join([d.page_content for d in docs])
    sources = list(set([d.metadata.get("source", "unknown") for d in docs]))

    llm = ChatOpenAI(model_name="gpt-4", temperature=0)

    prompt = f"""
    Answer ONLY from the context below.
    If answer is not present, return "NOT_FOUND".

    Context:
    {context}

    Question:
    {query}
    """

    response = llm.invoke(prompt)
    answer = response.content

    used_fallback = False

    if "NOT_FOUND" in answer or len(docs) == 0:
        used_fallback = True
        web_data = web_search(query)

        fallback_prompt = f"""
        Use this web data to answer:

        {web_data}

        Question: {query}
        """

        response = llm.invoke(fallback_prompt)
        answer = response.content

    return answer, sources, len(docs), used_fallback


# ==============================
# 🎨 STREAMLIT UI
# ==============================
st.set_page_config(page_title="RAG Chatbot", layout="wide")

st.title("📄 RAG Document Chatbot")

# -------- REBUILD BUTTON --------
if st.button("🔄 Rebuild Index"):
    st.cache_resource.clear()
    st.success("Cache cleared! Rebuilding on next run...")

# -------- LOAD DOCUMENTS --------
documents = []
file_names = []

# Load from docs folder
docs, names = load_docs_from_folder()
documents.extend(docs)
file_names.extend(names)

# Upload section
st.header("📂 Upload Document")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    uploaded_docs, uploaded_name = load_uploaded_file(uploaded_file)
    documents.extend(uploaded_docs)
    file_names.append(uploaded_name)
    st.success(f"Uploaded: {uploaded_name}")

# No documents case
if len(documents) == 0:
    st.warning("⚠️ No documents found. Upload a PDF or add files to docs/")
    st.stop()

# Debug info
st.write("📁 Files loaded:", file_names)

# -------- BUILD VECTOR DB --------
cache_key = generate_cache_key(file_names)
db, total_chunks = build_vectorstore(cache_key, documents)

# -------- QUERY SECTION --------
st.header("💬 Ask Questions")

with st.form("query_form"):
    query = st.text_input("Enter your question:")
    submit = st.form_submit_button("Submit")

if submit and query:
    with st.spinner("Thinking..."):
        answer, sources, chunk_count, fallback = get_rag_response(query, db)

    # -------- DETAILS --------
    st.subheader("📊 Retrieval Details")
    st.write(f"**📄 Files used:** {', '.join(sources)}")
    st.write(f"**📊 Chunks retrieved:** {chunk_count}")
    st.write(f"**📚 Total chunks in DB:** {total_chunks}")
    st.write(f"**🌐 Web fallback used:** {'Yes' if fallback else 'No'}")

    st.divider()

    # -------- ANSWER --------
    st.subheader("🤖 Answer")
    st.write(answer)