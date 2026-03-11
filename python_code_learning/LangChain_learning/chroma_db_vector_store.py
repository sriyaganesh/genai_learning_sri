import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings

# Initialize ChromaDB client (persistent storage)
#client = chromadb.Client() --
# client = chromadb.Client(Settings(persist_directory="./chroma_storage"))

# Persistent Chroma client
client = chromadb.PersistentClient(path="./chromadb_storage")

# Create or get collection
collection = client.get_or_create_collection(name="documents")

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Example texts
texts = [
    "ChromaDB is a vector database.",
    "Embeddings convert text into numerical vectors.",
    "Python is widely used for AI and machine learning."
]

# Create embeddings
embeddings = model.encode(texts).tolist()

# Add to ChromaDB
collection.add(
    documents=texts,
    embeddings=embeddings,
    ids=[f"id{i}" for i in range(len(texts))]
)

print("Data stored in ChromaDB successfully!")