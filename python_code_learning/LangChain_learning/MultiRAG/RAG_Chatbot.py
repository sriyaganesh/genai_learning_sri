import streamlit as st
import os
import faiss
import requests

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()


client = OpenAI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


st.set_page_config(layout="wide")

st.title("RAG Playground + Observatory")

# ------------------------
# Load Model
# ------------------------

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# ------------------------
# PDF Processing
# ------------------------

def process_pdfs(files):

    chunks = []
    sources = []

    for file in files:

        reader = PdfReader(file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

        for i in range(0,len(text),500):

            chunk = text[i:i+500]

            if chunk.strip():

                chunks.append(chunk)
                sources.append(file.name)

    return chunks,sources

# ------------------------
# Vector Index
# ------------------------

def create_index(chunks):

    embeddings = model.encode(chunks)

    index = faiss.IndexFlatL2(embeddings.shape[1])

    index.add(embeddings)

    return index

# ------------------------
# Hybrid Retrieval
# ------------------------

def hybrid_search(query,index,chunks,bm25):

    query_embedding = model.encode([query])

    distances,indices = index.search(query_embedding,3)

    vector_results = [chunks[i] for i in indices[0]]

    scores = distances[0]

    bm25_scores = bm25.get_scores(query.split())

    keyword_indices = sorted(
        range(len(bm25_scores)),
        key=lambda i: bm25_scores[i],
        reverse=True
    )[:3]

    keyword_results = [chunks[i] for i in keyword_indices]

    results = list(set(vector_results + keyword_results))

    return results, scores

# ------------------------
# Web Search
# ------------------------

def web_search(query):

    url = "https://serpapi.com/search.json"

    params = {
        "q":query,
        "api_key":SERPAPI_KEY
    }

    response = requests.get(url,params=params)

    results = response.json().get("organic_results",[])

    snippets=[]

    for r in results[:5]:

        snippet=r.get("snippet")

        if snippet:
            snippets.append(snippet)

    return "\n".join(snippets)

# ------------------------
# LLM Utilities
# ------------------------

def context_evaluator(query,context):

    prompt=f"""
Is this context sufficient to answer the query?

Query:
{query}

Context:
{context}

Answer only GOOD or BAD.
"""

    resp=client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return resp.choices[0].message.content


def agent_decision(query):

    prompt=f"""
Choose tool:

PDF_RAG
WEB_SEARCH

Query:
{query}

Return tool only.
"""

    resp=client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return resp.choices[0].message.content


def generate_answer(query,context):

    prompt=f"""
Answer the question using context.

Context:
{context}

Question:
{query}
"""

    resp=client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return resp.choices[0].message.content


# ------------------------
# UI Layout
# ------------------------

left,right = st.columns([2,1])

with left:

    rag_type = st.selectbox(
        "Select RAG Strategy",
        [
            "Simple RAG",
            "Corrective RAG",
            "Fallback RAG",
            "Web Search RAG",
            "Adaptive RAG",
            "Agentic RAG"
        ]
    )

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    question = st.chat_input("Ask your question")


with right:

    st.header("RAG Observatory")

    step1 = st.empty()
    step2 = st.empty()
    step3 = st.empty()
    step4 = st.empty()


if uploaded_files:

    chunks,sources = process_pdfs(uploaded_files)

    index = create_index(chunks)

    tokenized=[c.split() for c in chunks]

    bm25 = BM25Okapi(tokenized)

    if question:

        st.chat_message("user").write(question)

        step1.write("Step 1: Query received")

        retrieved, scores = hybrid_search(
            question,
            index,
            chunks,
            bm25
        )

        context="\n".join(retrieved)

        step2.write("Step 2: Retrieval complete")

        evaluation=context_evaluator(question,context)

        step3.write(f"Step 3: Context evaluation = {evaluation}")

        if rag_type == "Simple RAG":

            answer=generate_answer(question,context)

        elif rag_type == "Corrective RAG":

            answer=f"Context Quality: {evaluation}\n\n"

            answer+=generate_answer(question,context)

        elif rag_type == "Fallback RAG":

            if "BAD" in evaluation.upper():

                web=web_search(question)

                answer=generate_answer(question,web)

            else:

                answer=generate_answer(question,context)

        elif rag_type == "Web Search RAG":

            web=web_search(question)

            answer=generate_answer(question,web)

        elif rag_type == "Adaptive RAG":

            if "latest" in question.lower():

                web=web_search(question)

                answer=generate_answer(question,web)

            else:

                answer=generate_answer(question,context)

        else:

            tool=agent_decision(question)

            step4.write(f"Step 4: Agent selected {tool}")

            if "WEB" in tool.upper():

                web=web_search(question)

                answer=generate_answer(question,web)

            else:

                answer=generate_answer(question,context)

        st.chat_message("assistant").write(answer)

        st.subheader("Retrieved Chunks")

        for c in retrieved:

            st.write(c[:300]+"...")

        st.subheader("Similarity Scores")

        st.write(scores)

        st.subheader("Sources")

        for s in set(sources):

            st.write(s)
