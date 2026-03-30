# 🚀 GenAI Data Copilot

> An AI-powered Data Engineering & Analytics Copilot that transforms natural language into SQL, ETL pipelines, and actionable data insights using LLMs, RAG, and real-time data execution.

---

## 📌 Overview

GenAI Data Copilot is an intelligent assistant designed for data engineers, analysts, and business intelligence teams. It enables users to interact with structured and unstructured data using natural language and receive **accurate, structured, and execution-ready outputs**.

It combines:

- 🧠 Large Language Models (LLMs)
- 📊 Real-time Data Execution Engine (Pandas-based)
- 🔍 Retrieval-Augmented Generation (RAG)
- 🌐 DuckDuckGo-based web fallback
- 🕸️ Schema-aware reasoning engine

---

## ✨ Key Capabilities

### 🧠 AI Data Assistant
Ask questions in plain English and receive:
- SQL queries
- Data insights
- ETL pipeline logic
- Analytical breakdowns

---

### ⚡ Action-Based Intelligence Layer
Predefined structured actions:

- Generate SQL queries
- Design ETL pipelines
- Perform data profiling
- Generate dashboard logic
- Execute data analysis tasks

Each action returns:
- Structured response
- SQL (when applicable)
- Step-by-step explanation

---

### 📊 Real Data Execution Engine
Unlike typical AI tools, this system:
- Executes queries directly on uploaded datasets
- Performs real aggregations (MIN, MAX, AVG, COUNT)
- Prevents hallucinated numeric answers
- Maps natural language → dataframe operations

---

### 📚 RAG Knowledge Engine
- Supports PDF, CSV, TXT ingestion
- Semantic search using embeddings
- Context-aware retrieval
- Combines structured + unstructured intelligence

---

### 🌐 Intelligent Fallback System
If dataset context is insufficient:
- Uses DuckDuckGo search
- Enhances responses with external knowledge
- Ensures continuous answer generation

---

### 🕸️ Workspace Intelligence Layer
- Dataset preview
- Schema profiling
- Chat history tracking
- Optional relationship graph visualization

---

## 🏗️ Architecture

```text
User Query
   ↓
Streamlit UI Layer
   ↓
Intent Router (Action vs Ask AI)
   ↓
┌────────────────────────────────────────────┐
│ 1. Data Execution Engine (Pandas / SQL)    │
│ 2. RAG Retrieval Engine (Vector DB)        │
│ 3. LLM Reasoning Layer (GPT)               │
│ 4. Web Search Fallback (DuckDuckGo)        │
└────────────────────────────────────────────┘
   ↓
Structured Output (SQL / Insights / ETL)