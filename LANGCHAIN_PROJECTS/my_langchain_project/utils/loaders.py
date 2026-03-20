from langchain_community.document_loaders import PyPDFLoader, TextLoader,PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain_community.document_loaders import Docx2txtLoader
import io
import tempfile
import PyPDF2

def load_document(file_path):

    file_name = file_path.name
    suffix = file_name.split(".")[-1].lower()

    # Save uploaded file to temp
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp_file:
        tmp_file.write(file_path.getbuffer())
        temp_file_path = tmp_file.name

    # Load based on type
    if suffix == "pdf":
        loader = PyPDFLoader(temp_file_path)
    elif suffix == "txt":
        loader = TextLoader(temp_file_path, encoding="utf-8")
    elif suffix in ["docx", "doc"]:
        loader = UnstructuredWordDocumentLoader(temp_file_path)
    else:
        raise ValueError("Unsupported file type")
        return []
    
        
    
    return loader.load()  # <-- returns a list of documents with page_content
    
    
