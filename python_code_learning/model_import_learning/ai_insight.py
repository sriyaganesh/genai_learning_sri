import streamlit as st
from openai import OpenAI
from duckduckgo_search import DDGS
from youtube_transcript_api import YouTubeTranscriptApi
from docx import Document
from PyPDF2 import PdfReader
from pdf2docx import Converter
from docx2pdf import convert
import tempfile
import os
from dotenv import load_dotenv
load_dotenv()
# ---------------------------
# CONFIG
# ---------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


st.set_page_config(page_title="AI Utility Suite", layout="wide")

# ---------------------------
# SESSION STATE
# ---------------------------
if "mode" not in st.session_state:
    st.session_state.mode = "chat"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------
# UI DESIGN
# ---------------------------
st.markdown("""
<style>
body {background-color: #f4f8ff;}
.header-box {
    background: linear-gradient(90deg, #dbeafe, #e0f2fe);
    padding: 18px;
    border-radius: 14px;
    text-align:center;
    margin-bottom:20px;
}
.tool-button button {
    background-color:#93c5fd;
    font-size:14px;
    padding:6px 10px;
    border-radius:8px;
}
.chat-box {
    background:white;
    padding:20px;
    border-radius:14px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
<h2>🤖 AI Utility Suite</h2>
<p>Chat • Web Search • File Summarizer • Converters</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# MODE BUTTONS
# ---------------------------
cols = st.columns(5)

buttons = [
    ("💬 Chat", "chat"),
    ("🌍 Web Search", "search"),
    ("📄 Summarizer", "summarizer"),
    ("📑 Word→PDF", "word2pdf"),
    ("📘 PDF→Word", "pdf2word"),
]

for col, (label, value) in zip(cols, buttons):
    if col.button(label, use_container_width=True):
        st.session_state.mode = value

st.markdown("---")

# ====================================================
# 1️⃣ NORMAL CHAT
# ====================================================
def normal_chat(query):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content

# ====================================================
# 2️⃣ DUCKDUCKGO SEARCH
# ====================================================
def duckduckgo_search(query):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append(f"{r['title']} - {r['body']}")
    return "\n".join(results)

def search_chat(query):
    search_results = duckduckgo_search(query)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize search results clearly."},
            {"role": "user", "content": f"Results:\n{search_results}\n\nQuestion:{query}"}
        ]
    )
    return response.choices[0].message.content

# ====================================================
# 3️⃣ FILE SUMMARIZER
# ====================================================
def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize the following clearly in bullet points."},
            {"role": "user", "content": text[:15000]}
        ]
    )
    return response.choices[0].message.content

def extract_text_from_file(uploaded_file):
    if uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    elif uploaded_file.name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        return " ".join([page.extract_text() for page in reader.pages])

    elif uploaded_file.name.endswith(".docx"):
        doc = Document(uploaded_file)
        return " ".join([para.text for para in doc.paragraphs])

    else:
        return None

def extract_video_id(url):
    if "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    else:
        return url
    
def summarize_youtube(url):
    try:
        video_id = extract_video_id(url)

        transcript = YouTubeTranscriptApi().fetch(video_id)

        full_text = " ".join([item.text for item in transcript])

        return summarize_text(full_text)

    except Exception as e:
        return f"Error fetching transcript: {str(e)}"# ====================================================
# 4️⃣ WORD → PDF
# ====================================================
def convert_word_to_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
        tmp_docx.write(uploaded_file.read())
        tmp_docx_path = tmp_docx.name

    pdf_path = tmp_docx_path.replace(".docx", ".pdf")
    convert(tmp_docx_path, pdf_path)
    return pdf_path

# ====================================================
# 5️⃣ PDF → WORD
# ====================================================
def convert_pdf_to_word(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        tmp_pdf.write(uploaded_file.read())
        pdf_path = tmp_pdf.name

    docx_path = pdf_path.replace(".pdf", ".docx")
    cv = Converter(pdf_path)
    cv.convert(docx_path)
    cv.close()
    return docx_path

# ====================================================
# UI LOGIC
# ====================================================
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

if st.session_state.mode == "chat":
    query = st.text_input("Ask anything...")
    if st.button("Submit") and query:
        st.write(normal_chat(query))

elif st.session_state.mode == "search":
    query = st.text_input("Search the web...")
    if st.button("Search") and query:
        st.write(search_chat(query))

elif st.session_state.mode == "summarizer":
    option = st.radio("Choose Input Type:", ["Upload File", "YouTube Link"])

    if option == "Upload File":
        uploaded_file = st.file_uploader("Upload .txt / .pdf / .docx")
        if uploaded_file:
            text = extract_text_from_file(uploaded_file)
            summary = summarize_text(text)
            st.write(summary)

    else:
        url = st.text_input("Paste YouTube link")
        if st.button("Summarize Video") and url:
            st.write(summarize_youtube(url))

elif st.session_state.mode == "word2pdf":
    uploaded_file = st.file_uploader("Upload Word (.docx)")
    if uploaded_file:
        pdf_path = convert_word_to_pdf(uploaded_file)
        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="converted.pdf")

elif st.session_state.mode == "pdf2word":
    uploaded_file = st.file_uploader("Upload PDF")
    if uploaded_file:
        docx_path = convert_pdf_to_word(uploaded_file)
        with open(docx_path, "rb") as f:
            st.download_button("Download Word", f, file_name="converted.docx")

st.markdown('</div>', unsafe_allow_html=True)