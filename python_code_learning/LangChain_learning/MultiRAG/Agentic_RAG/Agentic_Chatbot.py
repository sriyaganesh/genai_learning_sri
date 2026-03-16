import os
import streamlit as st
import requests
import faiss
import numpy as np

from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import docx

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

client = OpenAI()

# ---------------------------------------
# LOAD EMBEDDING MODEL
# ---------------------------------------

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


# ---------------------------------------
# FILE TEXT EXTRACTION
# ---------------------------------------

def extract_text(files):

    documents = []

    for file in files:

        if file.type == "application/pdf":

            reader = PdfReader(file)
            text = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

            documents.append(text)

        elif file.type == "text/plain":

            documents.append(file.read().decode("utf-8"))

        elif "word" in file.type:

            doc = docx.Document(file)
            text = "\n".join([p.text for p in doc.paragraphs])
            documents.append(text)

    return documents


# ---------------------------------------
# FAST CHUNKING
# ---------------------------------------

def create_chunks(documents):

    chunk_size = 1200
    overlap = 200

    chunks = []

    for doc in documents:

        for i in range(0, len(doc), chunk_size - overlap):

            chunk = doc[i:i+chunk_size]

            if chunk.strip():
                chunks.append(chunk)

    MAX_CHUNKS = 300

    return chunks[:MAX_CHUNKS]


# ---------------------------------------
# CREATE VECTOR STORE
# ---------------------------------------

def create_vector_store(chunks):

    model = load_model()

    embeddings = model.encode(
        chunks,
        batch_size=32,
        show_progress_bar=True
    )

    embeddings = np.array(embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index, model


# ---------------------------------------
# RETRIEVAL WITH SCORES
# ---------------------------------------

def retrieve_chunks(query, chunks, index, model, k=4):

    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, k)

    results = [chunks[i] for i in indices[0]]

    scores = distances[0]

    return results, scores


# ---------------------------------------
# SMART ADAPTIVE ROUTER
# ---------------------------------------

def adaptive_router(query, chunks, index, model):

    retrieved, scores = retrieve_chunks(query, chunks, index, model)

    best_score = scores[0]

    DOCUMENT_THRESHOLD = 0.8
    HYBRID_THRESHOLD = 1.5

    if best_score < DOCUMENT_THRESHOLD:
        return "DOCUMENT"

    elif best_score < HYBRID_THRESHOLD:
        return "HYBRID"

    prompt = f"""
You are a routing agent.

Decide where the answer should come from.

Choices:
DOCUMENT
WEB
HYBRID

Question: {query}

Respond with only one word.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content.strip()


# ---------------------------------------
# WEB SEARCH
# ---------------------------------------

def web_search(query):

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


# ---------------------------------------
# ANSWER GENERATION
# ---------------------------------------

def generate_answer(query, context):

    prompt = f"""
Answer the question using the context.

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content


# ---------------------------------------
# SELF EVALUATION
# ---------------------------------------

def evaluate_answer(query, answer):

    prompt = f"""
Evaluate the answer quality.

Question:
{query}

Answer:
{answer}

Score:
Groundedness (0-10)
Completeness (0-10)

Decision: PASS or RETRY
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content


# ---------------------------------------
# AGENTIC RAG PIPELINE
# ---------------------------------------

def agentic_rag(query, chunks, index, model):

    route = adaptive_router(query, chunks, index, model)

    context = ""

    if route == "DOCUMENT":

        retrieved, _ = retrieve_chunks(query, chunks, index, model)

        context = "\n".join(retrieved)

    elif route == "WEB":

        context = web_search(query)

    else:

        retrieved, _ = retrieve_chunks(query, chunks, index, model)

        web = web_search(query)

        context = "\n".join(retrieved) + "\n\n" + web

    answer = generate_answer(query, context)

    evaluation = evaluate_answer(query, answer)

    if "RETRY" in evaluation:

        web = web_search(query)

        answer = generate_answer(query, context + "\n\n" + web)

    return route, answer, evaluation


# ---------------------------------------
# STREAMLIT UI
# ---------------------------------------

st.title("Adaptive Agentic RAG Chatbot")

# SESSION STATE INITIALIZATION
if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "index" not in st.session_state:
    st.session_state.index = None

if "model" not in st.session_state:
    st.session_state.model = None

uploaded_files = st.file_uploader(
    "Upload Documents",
    type=["pdf","txt","docx"],
    accept_multiple_files=True
)

# PROCESS DOCUMENTS
if uploaded_files and not st.session_state.documents_processed:

    with st.spinner("Extracting text..."):
        docs = extract_text(uploaded_files)

    with st.spinner("Creating chunks..."):
        chunks = create_chunks(docs)

    with st.spinner("Generating embeddings & FAISS index..."):
        index, model = create_vector_store(chunks)

    st.session_state.chunks = chunks
    st.session_state.index = index
    st.session_state.model = model
    st.session_state.documents_processed = True

    st.success(f"Indexed {len(chunks)} chunks successfully")

# QUERY INPUT
if st.session_state.documents_processed:

    query = st.text_input("Ask your question")

    if st.button("Submit") and query:

        with st.spinner("Running Adaptive Agentic RAG..."):

            route, answer, evaluation = agentic_rag(
                query,
                st.session_state.chunks,
                st.session_state.index,
                st.session_state.model
            )

        # SIDEBAR PIPELINE
        with st.sidebar:
            st.header("RAG Pipeline")
            st.write("1️⃣ Query Received")
            st.write(f"2️⃣ Router Decision: {route}")
            st.write("3️⃣ Retrieval")
            st.write("4️⃣ Answer Generation")
            st.write("5️⃣ Self Evaluation")

        st.subheader("Router Decision")
        st.write(route)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Self Evaluation")
        st.write(evaluation)