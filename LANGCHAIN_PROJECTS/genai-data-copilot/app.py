import streamlit as st
import pandas as pd

from rag_engine import init_vector_store, add_docs, retrieve_context
from doc_loader import load_file
from data_loader import load_csv, profile_data
from graph_engine import GraphEngine
from prompt_engine import build_prompt
from llm_engine import ask_llm
from memory import format_history
from search_engine import search_web

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(layout="wide")

# =========================================================
# UI THEME (BLACK + BLUE + RED ACCENT)
# =========================================================
st.markdown(
    """
    <style>

    .stApp {
        background-color: #000000;
        color: #d6e6ff;
    }

    .main-title {
        font-size: 22px;
        font-weight: 600;
        color: #4da3ff;
        padding: 10px;
        border-bottom: 2px solid #1f6feb;
        margin-bottom: 10px;
    }

    .panel {
        background-color: #050505;
        border: 1px solid #1f2a3a;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 12px;
    }

    .section-title {
        font-size: 14px;
        font-weight: 600;
        color: #4da3ff;
        margin-bottom: 8px;
    }

    textarea, input {
        background-color: #0a0a0a !important;
        color: #d6e6ff !important;
        border: 1px solid #1f6feb !important;
    }

    button {
        background-color: #1f6feb !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
    }

    button:hover {
        background-color: #2f81f7 !important;
    }

    /* WORKSPACE TABS */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #000000 !important;
        border-bottom: 1px solid #1f2a3a;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #000000 !important;
        color: #8aa0b8 !important;
    }

    .stTabs [aria-selected="true"] {
        color: #ff4d4d !important;
        border-bottom: 2px solid #ff4d4d !important;
        background-color: #000000 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">⚡ GenAI Data Copilot</div>', unsafe_allow_html=True)

# =========================================================
# STATE INIT
# =========================================================
if "db" not in st.session_state:
    st.session_state.db = init_vector_store()

if "history" not in st.session_state:
    st.session_state.history = []

if "df" not in st.session_state:
    st.session_state.df = None

if "output" not in st.session_state:
    st.session_state.output = None

graph = GraphEngine()

# =========================================================
# FILE UPLOAD
# =========================================================
uploaded_file = st.file_uploader("Upload CSV / PDF / TXT")

schema = []
relationships = []

if uploaded_file:
    ext = uploaded_file.name.split(".")[-1]

    if ext == "csv":
        df = load_csv(uploaded_file)
        st.session_state.df = df

        graph.load_schema(df)
        schema = graph.get_schema()
        relationships = graph.get_relationships()

    else:
        docs = load_file(uploaded_file)
        add_docs(st.session_state.db, docs)
        st.success("Document indexed into RAG")

# =========================================================
# LAYOUT
# =========================================================
left, right = st.columns([2.2, 1])

# =========================================================
# ACTION PROMPT (RESTORED STRONG SQL BEHAVIOR)
# =========================================================
def build_action_prompt(action, rag, data_ctx):
    return f"""
You are an expert Data Engineer, SQL Architect, and Analytics Consultant.

USER REQUEST:
{action}

DATA CONTEXT:
{data_ctx}

SCHEMA:
{schema}

RELATIONSHIPS:
{relationships}

DOCUMENT CONTEXT:
{rag}

CHAT HISTORY:
{format_history(st.session_state.history)}

INSTRUCTIONS:
- Provide structured but natural response
- ALWAYS generate SQL when applicable
- SQL must be production-ready
- Explain logic briefly before SQL
- If ETL → step-by-step pipeline
- If insights → patterns + KPIs + anomalies
"""
# =========================================================
# ASK AI PROMPT (RESTORED)
# =========================================================
def build_ai_prompt(query, rag, data_ctx):
    return f"""
You are a senior Data & AI assistant.

QUESTION:
{query}

DATA CONTEXT:
{data_ctx}

SCHEMA:
{schema}

DOCUMENT CONTEXT:
{rag}

CHAT HISTORY:
{format_history(st.session_state.history)}

RULES:
- Use SQL when question involves data
- Use schema if available
- Provide reasoning + examples
"""
# =========================================================
# LEFT PANEL
# =========================================================
with left:

    # ================= ACTIONS =================
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 Select Actions</div>', unsafe_allow_html=True)

    action = st.selectbox(
        "",
        [
            "Select...",
            "Design ETL",
            "Write SQL",
            "Analyze Pipeline",
            "Dashboard Suggestions",
            "Generate Insights",
            "Data Quality Check"
        ]
    )

    if action != "Select...":

        rag = retrieve_context(st.session_state.db, action)

        data_ctx = ""
        if st.session_state.df is not None:
            data_ctx = "\n".join(
                f"{c}: mean={st.session_state.df[c].mean()}"
                for c in st.session_state.df.columns
                if pd.api.types.is_numeric_dtype(st.session_state.df[c])
            )

        prompt = build_action_prompt(action, rag, data_ctx)

        st.session_state.output = ask_llm(prompt)
        st.session_state.history.append((action, st.session_state.output))

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= ASK AI =================
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🤖 Ask AI Assistant</div>', unsafe_allow_html=True)

    query = st.text_area("", placeholder="Ask anything about data, SQL, ETL, dashboards...")

    if st.button("Submit"):

        rag = retrieve_context(st.session_state.db, query)

        data_ctx = ""
        if st.session_state.df is not None:
            data_ctx = "\n".join(
                f"{c}: mean={st.session_state.df[c].mean()}"
                for c in st.session_state.df.columns
                if pd.api.types.is_numeric_dtype(st.session_state.df[c])
            )

        prompt = build_ai_prompt(query, rag, data_ctx)

        response = ask_llm(prompt)

        # fallback
        if not response or len(response) < 20:
            web = search_web(query)
            response = ask_llm(f"Web Data:\n{web}\nQ:{query}")

        st.session_state.output = response
        st.session_state.history.append((query, response))

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= OUTPUT =================
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📌 Output</div>', unsafe_allow_html=True)

    if st.session_state.output:
        st.write(st.session_state.output)
    else:
        st.caption("Run an action or Ask AI to generate output")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# RIGHT WORKSPACE
# =========================================================
with right:

    with st.expander("📊 Workspace", expanded=True):

        tab1, tab2, tab3, tab4 = st.tabs(
            ["Chat History", "Data", "Profile", "Graph"]
        )

        with tab1:
            for q, a in reversed(st.session_state.history):
                st.markdown(f"**Q:** {q}")
                st.caption(a)

        with tab2:
            if st.session_state.df is not None:
                st.dataframe(st.session_state.df.head(), use_container_width=True)

        with tab3:
            if st.session_state.df is not None:
                profile = profile_data(st.session_state.df)
                st.json(profile)

        with tab4:
            if relationships:
                for r in relationships:
                    st.write("🔗", r)