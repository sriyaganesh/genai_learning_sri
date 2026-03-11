from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

text=["Python is a high-level programming language.",
       "It is widely used for web development, data analysis, artificial intelligence, and scientific computing.",
       "Python's design philosophy emphasizes code readability and simplicity."]

# Create embeddings for the text
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_store=FAISS.from_texts(text, embedding_model)
vector_store.save_local("my_first_vecor_store")