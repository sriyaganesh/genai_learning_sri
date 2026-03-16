Adaptive Agentic RAG Chatbot

This project implements an Adaptive Agentic Retrieval-Augmented Generation (RAG) Chatbot built using Python, Streamlit, FAISS, Sentence Transformers, OpenAI, and SerpAPI. The system intelligently routes user queries to either document retrieval, web search, or a hybrid approach using a smart routing mechanism.

The chatbot supports document-based question answering by allowing users to upload files such as PDF, TXT, and DOCX, which are then processed, chunked, and converted into embeddings for efficient similarity search using FAISS vector indexing.

Key Features

1. Document Ingestion

Supports PDF, TXT, and DOCX uploads

Extracts text from documents

Splits documents into optimized chunks for embedding

2. Vector Embedding & Storage

Uses Sentence Transformers (all-MiniLM-L6-v2) for embeddings

Stores embeddings using FAISS for fast similarity search

3. Adaptive Routing
The system dynamically determines the best source for answering a query:

DOCUMENT → Answer using uploaded documents

WEB → Fetch information using SerpAPI web search

HYBRID → Combine document retrieval with web results

Routing is determined using:

Vector similarity scoring

LLM-based fallback routing

4. Retrieval-Augmented Generation (RAG)
Relevant document chunks are retrieved and used as context for the LLM to generate accurate responses.

5. Web Search Integration
If documents are insufficient, the system performs real-time web search using SerpAPI.

6. Agentic Self-Evaluation
After generating an answer, the system performs self-evaluation using the LLM to assess:

Groundedness

Completeness

If the answer quality is low, the system automatically retries using additional web context.

7. Interactive Streamlit Interface
The application provides a simple UI where users can:

Upload documents

Ask questions

View routing decisions

Inspect the RAG pipeline steps

Technology Stack

Python

Streamlit – UI interface

FAISS – Vector similarity search

Sentence Transformers – Embedding generation

OpenAI GPT models – Answer generation and evaluation

SerpAPI – Web search integration

PyPDF / python-docx – Document processing

Architecture Overview
User Query
    │
    ▼
Adaptive Router
(Vector Similarity + LLM Decision)
    │
 ┌──┴───────────┐
 │              │
DOCUMENT       WEB
 │              │
 ▼              ▼
Vector Search  Web Search
 │              │
 └─────HYBRID─────┘
        │
        ▼
Answer Generation (LLM)
        │
        ▼
Self Evaluation
        │
        ▼
Retry if needed
Use Cases

Document-based chatbots

Knowledge base assistants

Research assistants

Enterprise knowledge retrieval

Hybrid RAG systems