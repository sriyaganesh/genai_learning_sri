from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import ArxivLoader
from langchain_community.document_loaders import WikipediaLoader



print("Welcome to Langchain Learning")

# Text File LOad
text_file=TextLoader("C:/Users/SrividhyaGanesan/OneDrive - EPAM/Sri/AI/genai_learning_sri/python_code_learning/notes.txt")
result=text_file.load()
print(result)

print("\n")
# PDF Load
pdf_file=PyPDFLoader("C:/Users/SrividhyaGanesan/OneDrive - EPAM/Sri/AI/genai_learning_sri/python_code_learning/llm_details.pdf")
result_pdf=pdf_file.load()
print(result_pdf)


print("\n")
# Web page load
web_base=WebBaseLoader(web_path="https://www.geeksforgeeks.org/artificial-intelligence/large-language-model-llm/")
result_web=pdf_file.load()
print(result_web)



print("\n")
# # Research paper load


# research_paper = ArxivLoader(query="1706.03762")

# # result_arxiv = research_paper.load()

# # print(result_arxiv)

print("\n Wikipedia Load")


wiki=WikipediaLoader(query="Artificial intelligence")
print(wiki.load())



import os
import certifi
import sys
import io
from langchain_community.document_loaders import ArxivLoader

# Configure SSL certificates for Windows
os.environ['SSL_CERT_FILE'] = certifi.where()

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )

loader = ArxivLoader(query="1706.03762")

documents = loader.load()

print(documents)
print("arXiv loaded successfully")