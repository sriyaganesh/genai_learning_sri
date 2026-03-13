import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

def ingest_documents():

    docs = []

    for file in os.listdir("documents"):

        if file.endswith(".pdf"):

            loader = PyPDFLoader(f"documents/{file}")
            docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)

    embedding = OpenAIEmbeddings()

    db = Chroma.from_documents(
        chunks,
        embedding,
        persist_directory="vector_db"
    )

    db.persist()

    print("Medical documents ingested successfully")

if __name__ == "__main__":
    ingest_documents()