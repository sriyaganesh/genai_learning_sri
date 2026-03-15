import os
import streamlit as st

from pypdf import PdfReader
from openai import OpenAI
import requests
from sentence_transformers import SentenceTransformer
import faiss

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

client = OpenAI()


# -----------------------------
# LOAD PDF + CREATE FAISS INDEX
# -----------------------------

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_data
def load_pdfs_and_create_index(files):

    documents = []

    for file in files:

        reader = PdfReader(file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

        documents.append(text)

    # Chunking
    chunks = []

    for doc in documents:
        for i in range(0, len(doc), 500):

            chunk = doc[i:i+500]

            if chunk.strip():
                chunks.append(chunk)

    model = load_model()

    embeddings = model.encode(chunks)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index, chunks, model


# -----------------------------
# RETRIEVAL
# -----------------------------

def retrieve_relevant_chunks(query, chunks, index, model, top_k=3):

    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, top_k)

    relevant_chunks = [chunks[i] for i in indices[0]]

    return relevant_chunks


# -----------------------------
# ANSWER QUALITY CHECK
# -----------------------------

def is_answer_sufficient(query, answer):

    prompt = f"""
Question: {query}

Retrieved Answer:
{answer}

Is the retrieved answer sufficient?

Respond with:
YES or NO
plus a short explanation.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


# -----------------------------
# SERPAPI WEB SEARCH
# -----------------------------

def serpapi_search(query):

    url = "https://serpapi.com/search.json"

    params = {
        "q": query,
        "api_key": SERPAPI_API_KEY
    }

    resp = requests.get(url, params=params)

    results = resp.json().get("organic_results", [])

    snippets = []

    for result in results:

        snippet = result.get("snippet", "") or result.get("title", "")

        if snippet:
            snippets.append(snippet)

    if snippets:

        return "\n".join(snippets[:5])

    else:

        fallback_prompt = f"""
Web search failed.

Provide an answer based on general knowledge.

Question:
{query}

Clearly mention that this is fallback knowledge.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": fallback_prompt}]
        )

        return response.choices[0].message.content.strip()


# -----------------------------
# AGENTIC RAG PIPELINE
# -----------------------------

def answer_query(query, chunks, index, model):

    retrieved = retrieve_relevant_chunks(query, chunks, index, model)

    combined = "\n\n".join(retrieved)

    combined = combined[:3000]   # Prevent token overflow

    verdict = is_answer_sufficient(query, combined)

    if "YES" in verdict.upper():

        return f"""
### 📄 From PDFs

{combined}

**Verifier:** {verdict}
"""

    else:

        serp_result = serpapi_search(query)

        return f"""
### 🌐 From Web Search

{serp_result}

**Verifier:** {verdict}
"""


# -----------------------------
# STREAMLIT UI
# -----------------------------

st.title("Agentic RAG Demo (No Framework)")

uploaded_files = st.file_uploader(
    "Upload PDF documents",
    type="pdf",
    accept_multiple_files=True
)

if uploaded_files:

    with st.spinner("Processing PDFs..."):

        index, chunks, model = load_pdfs_and_create_index(uploaded_files)

    st.success("Documents indexed!")

    query = st.text_input("Enter your question:")

    if st.button("Get Answer") and query:

        with st.spinner("Generating answer..."):

            answer = answer_query(query, chunks, index, model)

        st.markdown(answer)
