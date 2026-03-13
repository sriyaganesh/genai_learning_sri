import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv()

# Load PDF
loader = PyPDFLoader("C:/Users/SrividhyaGanesan/OneDrive - EPAM/Sri/AI/genai_learning_sri/python_code_learning/llm_details.pdf")
documents = loader.load()

# Split text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = splitter.split_documents(documents)

# Embeddings
embeddings = OpenAIEmbeddings()

# Vector store
vectorstore = Chroma.from_documents(docs, embeddings)

retriever = vectorstore.as_retriever(search_kwargs={"k":3})

# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ---------------------------
# SELF RAG FUNCTION
# ---------------------------

def self_rag_query(question):

    print("First attempt without retrieval")

    first_answer = llm.invoke(f"Answer the question:/n{question}")
    first_answer = first_answer.content

    print(first_answer)

    if "I don't know" in first_answer or len(first_answer) < 40:

        print("/nLow confidence → retrieving documents")

        #docs = retriever.get_relevant_documents(question)
        docs = retriever.invoke(question)

        context = "/n".join([doc.page_content for doc in docs])

        prompt = f"""
Use the context below to answer the question.

Context:
{context}

Question:
{question}
"""

        final_answer = llm.invoke(prompt)

        return final_answer.content

    return first_answer


# Corrective RAG

def corrective_rag(question):

    # Step 1: First attempt (without retrieval)
    first_guess = llm.invoke(f"Try to answer: {question}").content

    print("First guess:", first_guess)

    # Step 2: Create sample documents
    docs = [
        Document(page_content="The largest cat species in the world is the liger."),
        Document(page_content="A liger is a hybrid of a male lion and a female tiger.")
    ]

    # Step 3: Create vector DB
    db = Chroma.from_documents(docs, embeddings)

    retriever = db.as_retriever()

    # Step 4: Retrieve relevant docs
    retrieved_docs = retriever.invoke(question)

    context = "\n".join([doc.page_content for doc in retrieved_docs])

    # Step 5: Correct the answer using retrieved context
    prompt = f"""
Use the following documents to correct the answer.

Documents:
{context}

Question:
{question}

Correct answer:
"""

    correction = llm.invoke(prompt).content

    return f"""
Original Answer:
{first_guess}

Corrected using documents:
{correction}
"""



# Run query
print("Running Self-RAG query...")
response = self_rag_query("What is the capital of France?")

print("/nFinal Answer:")
print(response)


print("\nRunning Corrective RAG query...")
print(corrective_rag("What is the largest cat?"))


## Fusion RAG

# -------------------------
# Documents
# -------------------------

docs = [
    Document(page_content="The sun is a star."),
    Document(page_content="The sun provides heat and light."),
    Document(page_content="The sun rises in the east.")
]

# -------------------------
# Embeddings + Vector DB
# -------------------------

db = Chroma.from_documents(docs, embeddings)

retriever = db.as_retriever()


# -------------------------
# Generate multiple queries
# -------------------------

def generate_queries(question):

    prompt = f"""
Generate 3 different search queries related to:

{question}
"""

    response = llm.invoke(prompt).content.split("\n")

    queries = [q.strip("- ") for q in response if q.strip() != ""]

    return queries


# -------------------------
# Fusion RAG Function
# -------------------------

def fusion_rag(question):

    queries = generate_queries(question)

    print("Generated Queries:", queries)

    all_docs = []

    for q in queries:

        retrieved_docs = retriever.invoke(q)

        all_docs.extend(retrieved_docs)

    # remove duplicates
    unique_docs = list({doc.page_content: doc for doc in all_docs}.values())

    context = "\n".join([doc.page_content for doc in unique_docs])

    prompt = f"""
Use the following information to answer the question.

Context:
{context}

Question:
{question}
"""

    answer = llm.invoke(prompt)

    return answer.content


# -------------------------
# Run Fusion RAG
# -------------------------

print(fusion_rag("Tell me about the sun"))



# Advanced RAG

def advanced_rag(question):

    print("Running Advanced RAG...")

    # Step 1: Topic guess (advanced step)
    guess_topic = llm.invoke(f"What topic is this question about? {question}").content

    # Step 2: Documents
    docs = [
        Document(page_content="Mercury is the closest planet to the sun."),
        Document(page_content="Venus is the second planet from the sun."),
        Document(page_content="Earth is our home planet."),
        Document(page_content="Mars is known as the red planet.")
    ]

    # Step 3: Vector database
    db = Chroma.from_documents(docs, embeddings)

    retriever = db.as_retriever()

    # Step 4: Retrieve documents
    retrieved_docs = retriever.invoke(question)

    context = "\n".join([doc.page_content for doc in retrieved_docs])

    # Step 5: Generate answer
    prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{question}
"""

    result = llm.invoke(prompt).content

    return f"Topic: {guess_topic}\nAnswer: {result}"


print(advanced_rag("Tell me about the planets in the solar system"))


# Speculative RAG
print("\nRunning Speculative RAG...")

def speculative_rag(question):

    # Step 1: Guess keyword (speculation step)
    guess_prompt = f"Extract the main keyword from this question: {question}"

    keyword = llm.invoke(guess_prompt).content.strip()

    print("Guessed Keyword:", keyword)

    # Step 2: Create documents
    docs = [
        Document(page_content="An elephant is the largest land animal."),
        Document(page_content="Elephants are herbivores and live in Africa and Asia."),
        Document(page_content="Blue whales are the largest animals but live in the ocean.")
    ]

    # Step 3: Create vector DB
    db = Chroma.from_documents(docs, embeddings)

    retriever = db.as_retriever(search_kwargs={"k":1})

    # Step 4: Retrieve documents using keyword
    retrieved_docs = retriever.invoke(keyword)

    context = "\n".join([doc.page_content for doc in retrieved_docs])

    # Step 5: Generate final answer
    prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{question}
"""

    answer = llm.invoke(prompt).content

    return answer


print(speculative_rag("What is the largest land animal?"))