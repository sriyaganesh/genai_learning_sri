import streamlit as st
from modules import summarizer, chatbot, code_assistant, learning
from utils.loaders import load_document
from utils.youtube import get_youtube_transcript
from utils.vectorstore import create_vectorstore_from_docs

st.set_page_config(page_title="Multi-Assistant AI Workspace", layout="wide")
st.title("🤖 Multi-Assistant AI Workspace")

# Sidebar: select module
module = st.sidebar.selectbox("Select Assistant", ["Summarizer", "Chatbot", "Code Assistant", "Learning"])

# ------------------ SUMMARIZER ------------------
if module == "Summarizer":
    st.header("📄 Summarizer")
    input_type = st.radio("Input Type", ["Text", "File", "YouTube URL"])
    
    if input_type == "Text":
        text = st.text_area("Enter text here")
        if st.button("Summarize"):
            if text.strip() == "":
                st.warning("Please enter some text.")
            else:
                summary = summarizer.summarize_text(text)
                st.subheader("Summary")
                st.write(summary)
                
    elif input_type == "File":
        # uploaded_file = st.file_uploader("Upload document", type=["pdf", "txt", "docx"])
        uploaded_file   = st.file_uploader("Upload your Resume (PDF or TXT)", type=["pdf","txt","docx"])

        if uploaded_file:
            docs = load_document(uploaded_file)
            
            text = " ".join([d.page_content for d in docs])
            if not text.strip():
                st.error("No text found in the uploaded document.")
            if st.button("Summarize"):
                summary = summarizer.summarize_text(text)
                st.subheader("Summary")
                st.write(summary)
                
    elif input_type == "YouTube URL":
        url = st.text_input("Paste YouTube video ID")
        if st.button("Summarize"):
            if url.strip() == "":
                st.warning("Please enter YouTube video ID.")
            else:
                transcript = get_youtube_transcript(url)
                summary = summarizer.summarize_text(transcript)
                st.subheader("Summary")
                st.write(summary)

# ------------------ CHATBOT ------------------
elif module == "Chatbot":
    st.header("💬 Agentic RAG Chatbot")
    
    uploaded_file = st.file_uploader("Upload document for RAG (optional)", type=["pdf", "txt", "docx"])
    query = st.text_input("Ask a question")

if st.button("Run Chatbot"):
    if query.strip() == "":
        st.warning("Please enter a question.")
    else:
        vectorstore = None

        # If a document is uploaded, create vectorstore
        if uploaded_file:
            docs = load_document(uploaded_file)
            vectorstore = create_vectorstore_from_docs(docs)

        # Initialize RAG agent (web search allowed by default)
        agent = chatbot.create_rag_agent(vectorstore=vectorstore, allow_web_search=True)
        response = agent(query)

        st.subheader("Answer")
        st.write(response)

# ------------------ CODE ASSISTANT ------------------
elif module == "Code Assistant":
    st.header("💻 Code Assistant")
    task = st.selectbox("Select Task", ["Generate", "Debug", "Explain", "Optimize"])
    code_input = st.text_area("Paste code (optional)")
    language = st.selectbox("Language", ["Python", "SQL", "Teradata"])
    
    if st.button("Run"):
        output = code_assistant.code_assistant(task, code_input, language)
        st.subheader("Result")
        st.code(output)

# ------------------ LEARNING ------------------
elif module == "Learning":
    st.header("📚 Learning Assistant")
    topic = st.text_input("Enter topic or upload document (optional for learning)")
    mode = st.selectbox("Mode", ["teach", "quiz", "evaluate"])
    user_answer = st.text_area("Your answer (for evaluate mode)")

    if st.button("Run"):
        if topic.strip() == "":
            st.warning("Please enter a topic or upload a document.")
        else:
            result = learning.learning_assistant(topic, mode, user_answer)
            st.subheader("Learning Output")
            st.write(result)