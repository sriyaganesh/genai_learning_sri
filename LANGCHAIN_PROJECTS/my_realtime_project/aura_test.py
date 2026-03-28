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

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASS")),
    
)

driver.verify_connectivity()
print("✅ Connected to Neo4j Aura")