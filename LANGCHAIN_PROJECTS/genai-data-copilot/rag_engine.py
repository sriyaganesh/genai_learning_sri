from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import sys
import certifi
import os

if sys.platform == "win32":
    os.environ["SSL_CERT_FILE"] = certifi.where()


def init_vector_store():
    embeddings = OpenAIEmbeddings()
    return FAISS.from_texts(["Initial context"], embeddings)

def add_docs(db, docs):
    db.add_documents(docs)

def retrieve_context(db, query):
    docs = db.similarity_search(query, k=5)
    return "\n".join([d.page_content for d in docs])