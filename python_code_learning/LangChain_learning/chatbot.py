from dotenv import load_dotenv
load_dotenv()

# LLM and embeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Text splitting
from langchain_text_splitters import CharacterTextSplitter

# PDF loader
from langchain_community.document_loaders import PyMuPDFLoader

# Vector store
from langchain_community.vectorstores import FAISS

# Conversational chain
from langchain_classic.chains import ConversationalRetrievalChain


# STEP 1: Load the PDF
loader = PyMuPDFLoader("C:/Users/SrividhyaGanesan/OneDrive - EPAM/Sri/AI/genai_learning_sri/python_code_learning/llm_details.pdf")
documents = loader.load()


# STEP 2: Split text into chunks
text_splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

docs = text_splitter.split_documents(documents)


# STEP 3: Create embeddings
embeddings = OpenAIEmbeddings()


# STEP 4: Create FAISS vector database
vectorstore = FAISS.from_documents(docs, embeddings)


# STEP 5: Create retriever
retriever = vectorstore.as_retriever()


# STEP 6: Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# STEP 7: Create Conversational Retrieval Chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=retriever
)


print("\n📄 PDF Chatbot Ready!")
print("Type 'exit' to stop.\n")


# Store chat history manually
chat_history = []


# STEP 8: Chat loop
while True:

    query = input("You: ")

    if query.lower() == "exit":
        print("Chatbot stopped.")
        break

    result = qa_chain.invoke({
        "question": query,
        "chat_history": chat_history
    })

    answer = result["answer"]

    print("\nBot:", answer)

    # Save conversation history
    chat_history.append((query, answer))
