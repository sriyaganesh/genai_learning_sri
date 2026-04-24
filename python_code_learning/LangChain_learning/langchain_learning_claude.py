"""
LangChain Document Loaders Explorer
Demonstrates loading documents from text files, CSV, JSON, PDFs, arXiv papers,
web pages, and Wikipedia.
"""

import os
import json
import csv

# ── Sample files created at runtime ───────────────────────────────────────────

SAMPLE_TXT = "sample.txt"
SAMPLE_CSV = "sample.csv"
SAMPLE_JSON = "sample.json"

def create_sample_files():
    with open(SAMPLE_TXT, "w") as f:
        f.write("LangChain makes it easy to build LLM-powered applications.\n")
        f.write("It provides loaders, chains, agents, and memory components.\n")
        f.write("Document loaders ingest data from many sources into a standard format.\n")

    with open(SAMPLE_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "role"])
        writer.writeheader()
        writer.writerows([
            {"name": "Alice", "role": "Data Scientist"},
            {"name": "Bob",   "role": "ML Engineer"},
            {"name": "Carol", "role": "LLM Researcher"},
        ])

    with open(SAMPLE_JSON, "w") as f:
        json.dump([
            {"id": 1, "topic": "Prompt Engineering", "level": "beginner"},
            {"id": 2, "topic": "RAG Pipelines",      "level": "intermediate"},
            {"id": 3, "topic": "Agent Frameworks",   "level": "advanced"},
        ], f, indent=2)

def cleanup_sample_files():
    for path in [SAMPLE_TXT, SAMPLE_CSV, SAMPLE_JSON]:
        if os.path.exists(path):
            os.remove(path)

# ── Loader demos ──────────────────────────────────────────────────────────────

def demo_text_loader():
    print("\n" + "=" * 55)
    print("1. TextLoader — load a plain .txt file")
    print("=" * 55)
    from langchain_community.document_loaders import TextLoader

    loader = TextLoader(SAMPLE_TXT)
    docs = loader.load()
    for doc in docs:
        print(f"  Source  : {doc.metadata.get('source')}")
        print(f"  Content : {doc.page_content.strip()}")


def demo_csv_loader():
    print("\n" + "=" * 55)
    print("2. CSVLoader — load rows from a CSV file")
    print("=" * 55)
    from langchain_community.document_loaders.csv_loader import CSVLoader

    loader = CSVLoader(SAMPLE_CSV)
    docs = loader.load()
    for doc in docs:
        print(f"  Row     : {doc.page_content.strip()}")


def demo_json_loader():
    print("\n" + "=" * 55)
    print("3. JSONLoader — extract fields from a JSON file")
    print("=" * 55)
    from langchain_community.document_loaders import JSONLoader

    # jq-style path: pull the 'topic' field from each array element
    loader = JSONLoader(file_path=SAMPLE_JSON, jq_schema=".[].topic", text_content=True)
    docs = loader.load()
    for doc in docs:
        print(f"  Topic   : {doc.page_content.strip()}")


def demo_web_loader():
    print("\n" + "=" * 55)
    print("4. WebBaseLoader — scrape a public web page")
    print("=" * 55)
    from langchain_community.document_loaders import WebBaseLoader

    loader = WebBaseLoader("https://en.wikipedia.org/wiki/LangChain")
    docs = loader.load()
    snippet = docs[0].page_content[:300].replace("\n", " ").strip()
    print(f"  Source  : {docs[0].metadata.get('source')}")
    print(f"  Snippet : {snippet}...")


def demo_wikipedia_loader():
    print("\n" + "=" * 55)
    print("5. WikipediaLoader — load a Wikipedia article summary")
    print("=" * 55)
    from langchain_community.document_loaders import WikipediaLoader

    loader = WikipediaLoader(query="Retrieval-Augmented Generation", load_max_docs=1)
    docs = loader.load()
    snippet = docs[0].page_content[:300].replace("\n", " ").strip()
    print(f"  Title   : {docs[0].metadata.get('title')}")
    print(f"  Snippet : {snippet}...")


def demo_pdf_loader():
    print("\n" + "=" * 55)
    print("7. PyPDFLoader — load pages from a PDF file")
    print("=" * 55)
    from langchain_community.document_loaders import PyPDFLoader

    # Uses a small, freely available PDF from arxiv for the demo
    pdf_url = "https://arxiv.org/pdf/1706.03762"   # "Attention Is All You Need"
    loader = PyPDFLoader(pdf_url)
    docs = loader.load()
    print(f"  Pages loaded : {len(docs)}")
    snippet = docs[0].page_content[:300].replace("\n", " ").strip()
    print(f"  Page 1 snippet : {snippet}...")


def demo_arxiv_loader():
    print("\n" + "=" * 55)
    print("8. ArxivLoader — fetch a paper from arXiv by ID")
    print("=" * 55)
    from langchain_community.document_loaders import ArxivLoader

    # 1706.03762 = "Attention Is All You Need"
    loader = ArxivLoader(query="1706.03762", load_max_docs=1)
    docs = loader.load()
    meta = docs[0].metadata
    snippet = docs[0].page_content[:300].replace("\n", " ").strip()
    print(f"  Title    : {meta.get('Title')}")
    print(f"  Authors  : {meta.get('Authors')}")
    print(f"  Published: {meta.get('Published')}")
    print(f"  Snippet  : {snippet}...")


def demo_directory_loader():
    print("\n" + "=" * 55)
    print("6. DirectoryLoader — load all .txt files in a folder")
    print("=" * 55)
    from langchain_community.document_loaders import DirectoryLoader, TextLoader

    loader = DirectoryLoader(".", glob="*.txt", loader_cls=TextLoader)
    docs = loader.load()
    print(f"  Files loaded : {len(docs)}")
    for doc in docs:
        print(f"  Source : {doc.metadata.get('source')}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║        LangChain Document Loaders Explorer           ║")
    print("╚══════════════════════════════════════════════════════╝")

    create_sample_files()

    try:
        demo_text_loader()
        demo_csv_loader()
        demo_json_loader()
        demo_directory_loader()
        demo_web_loader()
        demo_wikipedia_loader()
        demo_pdf_loader()
        demo_arxiv_loader()
    finally:
        cleanup_sample_files()

    print("\n✓ All loaders demonstrated successfully.\n")


if __name__ == "__main__":
    main()
