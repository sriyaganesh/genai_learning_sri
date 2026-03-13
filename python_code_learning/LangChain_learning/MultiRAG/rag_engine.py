import os
import streamlit as st

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# -----------------------------
# LLM + Embeddings
# -----------------------------

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

embedding = OpenAIEmbeddings()


# -----------------------------
# Sidebar - RAG Explanation
# -----------------------------

st.sidebar.title("RAG Strategy Guide")

rag_explanations = {

"Speculative RAG":[
"Step 1: Identify topic of the question",
"Step 2: Predict possible knowledge area",
"Step 3: Guide retrieval using topic"
],

"Fusion RAG":[
"Step 1: Generate multiple search queries",
"Step 2: Retrieve documents for each query",
"Step 3: Merge all retrieved results",
"Step 4: Build enriched context"
],

"Self RAG":[
"Step 1: Retrieve relevant documents",
"Step 2: Provide context to LLM",
"Step 3: LLM generates grounded answer"
],

"Corrective RAG":[
"Step 1: Retrieve documents",
"Step 2: Generate initial answer",
"Step 3: Improve answer using context"
],

"Advanced RAG":[
"Step 1: Retrieve documents",
"Step 2: Provide context to LLM",
"Step 3: Generate structured medical response"
],

"Multi RAG Pipeline":[
"Step 1: Speculative RAG → identify topic",
"Step 2: Fusion RAG → multi query retrieval",
"Step 3: Self RAG → generate answer",
"Step 4: Advanced RAG → structured clinical response"
]

}


# -----------------------------
# Load Default Docs
# -----------------------------

def load_default_documents():

    docs = []
    folder = "documents"

    if os.path.exists(folder):

        for file in os.listdir(folder):

            if file.endswith(".pdf"):

                loader = PyPDFLoader(os.path.join(folder, file))
                docs.extend(loader.load())

    return docs


# -----------------------------
# Load Uploaded Docs
# -----------------------------

def load_uploaded_documents(files):

    docs = []

    for file in files:

        os.makedirs("temp", exist_ok=True)

        path = os.path.join("temp", file.name)

        with open(path, "wb") as f:
            f.write(file.getbuffer())

        loader = PyPDFLoader(path)

        docs.extend(loader.load())

    return docs


# -----------------------------
# Split Docs
# -----------------------------

def split_documents(docs):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return splitter.split_documents(docs)


# -----------------------------
# Vector DB
# -----------------------------

def create_vector_db(chunks):

    db = Chroma.from_documents(chunks, embedding)

    return db.as_retriever(search_kwargs={"k":3})


# -----------------------------
# RAG METHODS
# -----------------------------

def speculative_rag(question, steps):

    steps["Step 1"] = "Identifying medical topic"

    topic = llm.invoke(f"Identify the medical topic: {question}").content

    steps["Topic Identified"] = topic

    return topic


def fusion_rag(question, retriever, steps):

    steps["Step 2"] = "Generating multiple search queries"

    queries = llm.invoke(
        f"Generate 3 search queries for: {question}"
    ).content.split("\n")

    steps["Generated Queries"] = queries

    docs = []

    steps["Step 3"] = "Retrieving documents"

    for q in queries:

        results = retriever.invoke(q)

        docs.extend(results)

    context = "\n".join([d.page_content for d in docs])

    steps["Context Created"] = context[:500]

    return context


def self_rag(question, context, steps):

    steps["Step 4"] = "Generating grounded answer"

    answer = llm.invoke(
        f"""
Context:
{context}

Question:
{question}

Answer:
"""
    ).content

    steps["Generated Answer"] = answer

    return answer


def corrective_rag(question, retriever, steps):

    steps["Step 1"] = "Retrieving documents"

    docs = retriever.invoke(question)

    context = "\n".join([d.page_content for d in docs])

    steps["Step 2"] = "Improving answer"

    improved = llm.invoke(
        f"""
Improve answer using context:

{context}

Question:
{question}
"""
    ).content

    steps["Improved Answer"] = improved

    return improved


def advanced_rag(question, context, steps):

    steps["Step 1"] = "Generating structured clinical response"

    final = llm.invoke(
        f"""
You are a clinical assistant.

Context:
{context}

Question:
{question}

Provide structured response:

Overview
Symptoms
Treatment
Clinical Notes
"""
    ).content

    steps["Final Structured Answer"] = final

    return final


# -----------------------------
# MULTI RAG PIPELINE
# -----------------------------

def multi_rag_pipeline(question, retriever):

    steps = {}

    topic = speculative_rag(question, steps)

    context = fusion_rag(question, retriever, steps)

    answer = self_rag(question, context, steps)

    final = advanced_rag(question, context, steps)

    return final, steps


# -----------------------------
# STREAMLIT UI
# -----------------------------

st.title("AI Medical Knowledge Assistant")

st.write("Ask questions from clinical medical documents.")


question = st.text_input("Enter your medical question")


rag_type = st.selectbox(
    "Select RAG Strategy",
    list(rag_explanations.keys())
)


uploaded_files = st.file_uploader(
    "Upload additional PDFs",
    type="pdf",
    accept_multiple_files=True
)


submit = st.button("Submit")


# -----------------------------
# SHOW RAG EXPLANATION
# -----------------------------

st.sidebar.subheader("Pipeline Steps")

for step in rag_explanations[rag_type]:

    st.sidebar.write(step)


# -----------------------------
# RUN PIPELINE
# -----------------------------

if submit and question:

    steps = {}

    with st.status("Running RAG Pipeline...", expanded=True):

        st.write("Loading documents")

        docs = load_default_documents()

        if uploaded_files:

            st.write("Adding uploaded documents")

            docs.extend(load_uploaded_documents(uploaded_files))

        st.write("Splitting documents")

        chunks = split_documents(docs)

        st.write("Creating vector database")

        retriever = create_vector_db(chunks)

        st.write("Executing RAG strategy")

        if rag_type == "Speculative RAG":

            result = speculative_rag(question, steps)

        elif rag_type == "Fusion RAG":

            result = fusion_rag(question, retriever, steps)

        elif rag_type == "Self RAG":

            docs = retriever.invoke(question)

            context = "\n".join([d.page_content for d in docs])

            result = self_rag(question, context, steps)

        elif rag_type == "Corrective RAG":

            result = corrective_rag(question, retriever, steps)

        elif rag_type == "Advanced RAG":

            docs = retriever.invoke(question)

            context = "\n".join([d.page_content for d in docs])

            result = advanced_rag(question, context, steps)

        else:

            result, steps = multi_rag_pipeline(question, retriever)


    st.subheader("Final Answer")

    st.write(result)


    # -----------------------------
    # SIDEBAR RUNTIME LOGS
    # -----------------------------

    st.sidebar.markdown("---")
    st.sidebar.subheader("Execution Logs")

    for step, value in steps.items():

        st.sidebar.markdown(f"**{step}**")

        st.sidebar.write(value)