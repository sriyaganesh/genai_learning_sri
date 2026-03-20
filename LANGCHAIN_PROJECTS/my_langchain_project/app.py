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

    # Optional document upload
    uploaded_file = st.file_uploader("Upload a document (optional)", type=["pdf", "txt", "docx"])
    topic = st.text_input("Enter topic or leave blank to use uploaded document")
    mode = st.selectbox("Select mode", ["teach", "quiz", "evaluate"])

    user_answer = ""
    if mode == "evaluate":
        user_answer = st.text_area("Enter your answer for evaluation")

    # Initialize session state for quiz
    if "quiz_active" not in st.session_state:
        st.session_state.quiz_active = False
        st.session_state.mcqs = []
        st.session_state.current_question = 0
        st.session_state.user_answers = []
        st.session_state.feedbacks = []

    # START QUIZ
    if mode == "quiz":
        start_quiz_clicked = st.button("Start Quiz")
        if start_quiz_clicked or st.session_state.quiz_active:
            if start_quiz_clicked:
                docs_text = load_document(uploaded_file) if uploaded_file else None
                quiz_topic = topic if topic.strip() else "N/A"
                mcqs = learning.generate_mcq_quiz(topic=quiz_topic, docs=docs_text, num_questions=10)

                if not mcqs:
                    st.warning("No questions generated.")
                else:
                    st.session_state.quiz_active = True
                    st.session_state.mcqs = mcqs
                    st.session_state.current_question = 0
                    st.session_state.user_answers = []
                    st.session_state.feedbacks = []

            # Display current question
            if st.session_state.quiz_active:
                q_idx = st.session_state.current_question
                mcq = st.session_state.mcqs[q_idx]

                st.markdown(f"### Question {q_idx + 1}: {mcq['question']}")
                selected_option = st.radio("Choose your answer", mcq["options"], key=f"q{q_idx}")

                submit_clicked = st.button("Submit Answer", key=f"submit_{q_idx}")
                if submit_clicked:
                    # Validate correct answer
                    try:
                        correct_index = ord(mcq["answer"].upper()) - ord("A")
                        correct_option = mcq["options"][correct_index]
                    except:
                        correct_option = "N/A"

                    feedback_text = f"Correct answer: {mcq['answer']} - {correct_option}"
                    if selected_option == correct_option:
                        feedback_text += "\n✅ Your answer is correct!"
                    else:
                        feedback_text += "\n❌ Your answer is incorrect."

                    st.session_state.user_answers.append(selected_option)
                    st.session_state.feedbacks.append(feedback_text)
                    st.markdown("**Feedback:**")
                    st.write(feedback_text)

                    # Advance to next question
                    if q_idx + 1 < len(st.session_state.mcqs):
                        st.session_state.current_question += 1
                    else:
                        st.session_state.quiz_active = False

        # QUIZ SUMMARY
        if not st.session_state.quiz_active and st.session_state.feedbacks:
            st.header("Quiz Summary & Insights")
            for i, (mcq, ans, fb) in enumerate(zip(st.session_state.mcqs, st.session_state.user_answers, st.session_state.feedbacks)):
                st.markdown(f"**Q{i+1}:** {mcq['question']}")
                st.markdown(f"Your answer: {ans}")
                st.markdown(f"Feedback: {fb}")

            overall_insights = learning.learning_assistant(
                topic=topic,
                mode="evaluate",
                user_answer="\n".join(st.session_state.user_answers),
                docs=None
            )
            st.subheader("Overall Insights & Areas for Improvement")
            st.write(overall_insights)

    # RUN OTHER MODES
    else:
        if st.button("Run"):
            if not topic.strip() and not uploaded_file:
                st.warning("Please enter a topic or upload a document.")
            else:
                doc_content = load_document(uploaded_file) if uploaded_file else None
                result = learning.learning_assistant(
                    topic=topic,
                    mode=mode,
                    user_answer=user_answer,
                    docs=doc_content
                )
                st.subheader("Learning Output")
                st.write(result)