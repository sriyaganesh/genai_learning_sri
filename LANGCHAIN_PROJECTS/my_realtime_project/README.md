# 📄 RAG Document Chatbot

A **Retrieval-Augmented Generation (RAG)** chatbot built with **Python**, **Streamlit**, and **LangChain**.  
It allows you to ask questions from PDF documents stored locally or uploaded dynamically. If the answer is not found in the documents, it automatically searches the web as a fallback.

---

## 🔹 Features

- Load PDFs from a local `docs/` folder  
- Upload PDFs dynamically via the web interface  
- Semantic search with **FAISS vector store**  
- Answer questions using **OpenAI GPT-4**  
- Web search fallback using **DuckDuckGo**  
- Displays retrieval details:
  - Source files used  
  - Number of chunks retrieved  
  - Total chunks in the vector DB  
  - Whether fallback was used  
- Submit queries with a **button**  
- Rebuild vector store with a **“Rebuild Index” button**
