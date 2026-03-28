from neo4j import GraphDatabase

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

from neo4j import GraphDatabase

load_dotenv()

DOCS_PATH = "docs"

# ==============================
# 🔗 NEO4J CONFIG
# ==============================
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

from neo4j import GraphDatabase
import os

# driver = GraphDatabase.driver(
#     os.getenv("NEO4J_URI"),
#    # auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASS")),
#     auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")),
    
# )


print("URI:", URI)
print("USER:", USER)
print("PASS:", "SET" if PASSWORD else "MISSING")

#driver.verify_connectivity()
print("✅ Connected to Neo4j Aura")



from neo4j import GraphDatabase
import certifi

# Fix SSL for Neo4j on Windows
import sys
if sys.platform == "win32":
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())

driver = GraphDatabase.driver(
    "neo4j+s://8be6b618.databases.neo4j.io",
    auth=(USER, PASSWORD)
)

with driver.session() as session:
    result = session.run("RETURN 1 AS num")
    print(result.single()["num"])