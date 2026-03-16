import os
import streamlit as st
import requests
import faiss
import numpy as np
import hashlib
import docx

from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

client = OpenAI()

# -----------------------------
# EMBEDDING MODEL
# -----------------------------

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# -----------------------------
# HELPER: FILE HASH
# -----------------------------

def get_file_hash(files):
    m = hashlib.md5()

    for f in files:
        m.update(f.name.encode())
        m.update(f.getvalue())

    return m.hexdigest()

# -----------------------------
# TEXT EXTRACTION
# -----------------------------

def extract_text(files):

    docs = []

    for file in files:

        if file.type == "application/pdf":

            reader = PdfReader(file)

            text = ""

            for i, page in enumerate(reader.pages):

                page_text = page.extract_text()

                if page_text:
                    text += f"[Page {i}] {page_text}\n"

            docs.append(text)

        elif file.type == "text/plain":

            docs.append(file.read().decode("utf-8"))

        elif "word" in file.type:

            doc = docx.Document(file)
            text = "\n".join([p.text for p in doc.paragraphs])
            docs.append(text)

    return docs

# -----------------------------
# CHUNKING
# -----------------------------

def create_chunks(docs):

    chunk_size = 1200
    overlap = 200

    chunks = []

    for doc in docs:

        for i in range(0, len(doc), chunk_size-overlap):

            chunk = doc[i:i+chunk_size]

            if chunk.strip():

                chunks.append({
                    "timestamp": f"segment_{i}",
                    "text": chunk
                })

    return chunks[:300]

# -----------------------------
# VECTOR STORE
# -----------------------------

def build_index(chunks):

    texts = [c["text"] for c in chunks]

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True
    )

    embeddings = np.array(embeddings)

    index = faiss.IndexFlatL2(embeddings.shape[1])

    index.add(embeddings)

    return index

# -----------------------------
# RETRIEVAL
# -----------------------------

def retrieve(query):

    query_embedding = model.encode([query])

    distances, indices = st.session_state.index.search(query_embedding, 4)

    return [st.session_state.chunks[i] for i in indices[0]]

# -----------------------------
# ADAPTIVE ROUTER
# -----------------------------

def adaptive_router(query):

    prompt = f"""
Decide retrieval strategy.

Options:
DOCUMENT
WEB
HYBRID

Question: {query}

Return one word.
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return res.choices[0].message.content.strip()

# -----------------------------
# SERPAPI SEARCH
# -----------------------------

def serpapi_search(query):

    url = "https://serpapi.com/search.json"

    params = {
        "q": query,
        "api_key": SERPAPI_API_KEY
    }

    response = requests.get(url, params=params)

    results = response.json().get("organic_results", [])

    snippets = []

    for r in results:

        snippet = r.get("snippet") or r.get("title")

        if snippet:
            snippets.append(snippet)

    return "\n".join(snippets[:5])

# -----------------------------
# ANSWER GENERATION
# -----------------------------

def generate_answer(query, context):

    prompt = f"""
Answer the question using context.

Context:
{context}

Question:
{query}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return res.choices[0].message.content

# -----------------------------
# SELF EVALUATION
# -----------------------------

def evaluate_answer(query, answer):

    prompt = f"""
Evaluate answer quality.

Question: {query}

Answer: {answer}

Score groundedness (0-10)
Score completeness (0-10)

Decision: PASS or RETRY
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return res.choices[0].message.content

# -----------------------------
# AGENTIC RAG
# -----------------------------

def agentic_rag(query):

    route = adaptive_router(query)

    if route == "DOCUMENT":

        retrieved = retrieve(query)

        context = "\n".join([c["text"] for c in retrieved])

    elif route == "WEB":

        context = serpapi_search(query)

    else:

        retrieved = retrieve(query)

        web = serpapi_search(query)

        context = "\n".join([c["text"] for c in retrieved]) + "\n\n" + web

    answer = generate_answer(query, context)

    evaluation = evaluate_answer(query, answer)

    if "RETRY" in evaluation:

        context += "\n\n" + serpapi_search(query)

        answer = generate_answer(query, context)

    return route, answer, evaluation


# =============================
# STREAMLIT UI
# =============================

st.title("Adaptive Agentic RAG Chatbot")

uploaded_files = st.file_uploader(
    "Upload documents",
    type=["pdf","txt","docx"],
    accept_multiple_files=True
)

if uploaded_files:

    file_hash = get_file_hash(uploaded_files)

    # Only process if new files
    if "file_hash" not in st.session_state or st.session_state.file_hash != file_hash:

        with st.spinner("Processing documents..."):

            docs = extract_text(uploaded_files)

            chunks = create_chunks(docs)

            index = build_index(chunks)

            st.session_state.index = index
            st.session_state.chunks = chunks
            st.session_state.file_hash = file_hash

        st.success(f"Indexed {len(chunks)} chunks")

# Ask questions without reprocessing
if "index" in st.session_state:

    query = st.text_input("Ask your question")

    if st.button("Submit") and query:

        with st.spinner("Generating answer..."):

            route, answer, evaluation = agentic_rag(query)

        st.subheader("Router Decision")
        st.write(route)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Self Evaluation")
        st.write(evaluation)