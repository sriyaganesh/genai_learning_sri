import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Validate API Key
# -----------------------------
if not os.getenv("OPENAI_API_KEY"):
    st.error("❌ OPENAI_API_KEY not found. Please set it in .env file")
    st.stop()

# -----------------------------
# Streamlit Config
# -----------------------------
st.set_page_config(page_title="AI Coding Assistant", layout="wide")
st.title("💻 AI Coding Assistant")

# -----------------------------
# TOP PANEL - OPTIONS
# -----------------------------
st.subheader("⚙️ Configuration")

col1, col2, col3 = st.columns(3)

with col1:
    mode = st.selectbox(
        "Select Mode",
        ["Generate Code", "Explain Code", "Debug Code", "Optimize Code"]
    )

with col2:
    language = st.selectbox(
        "Select Language",
        ["Python", "SQL", "Teradata"]
    )

with col3:
    model_choice = st.selectbox(
        "Choose Model",
        ["gpt-4o", "gpt-4o-mini"]
    )

# -----------------------------
# Initialize LLM
# -----------------------------
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model=model_choice,
    temperature=0.3
)

# -----------------------------
# Prompt Templates
# -----------------------------
templates = {
    "Generate Code": """
You are an expert {language} developer.

Task: {input}

Provide:
1. Clean, production-ready {language} code
2. Comments
3. Example usage (if applicable)
""",

    "Explain Code": """
You are an expert {language} developer.

Explain the following {language} code clearly:
{input}
""",

    "Debug Code": """
You are an expert {language} debugger.

Fix the issues in the following {language} code:
{input}

Provide corrected code and explanation.
""",

    "Optimize Code": """
You are an expert in optimizing {language} code.

Optimize the following code:
{input}

Provide improved code and explanation.
"""
}

prompt = PromptTemplate(
    input_variables=["input", "language"],
    template=templates[mode]
)

chain = prompt | llm

# -----------------------------
# Session State for History
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# MAIN INPUT SECTION
# -----------------------------
st.subheader("🧠 Input")

user_input = st.text_area("Enter your request or code:")

col_btn1, col_btn2 = st.columns(2)
generate_btn = col_btn1.button("Generate")
#run_btn = col_btn2.button("Run Code (Python Only)")

# -----------------------------
# Generate Response
# -----------------------------
if generate_btn:
    if user_input.strip() == "":
        st.warning("Please enter input")
    else:
        with st.spinner("Generating..."):
            try:
                response = chain.invoke({
                    "input": user_input,
                    "language": language
                })
                output = response.content

                st.session_state.history.append({
                    "input": user_input,
                    "output": output,
                    "language": language
                })

                st.success("✅ Generated Successfully")

            except Exception as e:
                st.error(f"❌ Error: {e}")

# -----------------------------
# Run Code (Python Only)
# -----------------------------
# if run_btn:
#     if language != "Python":
#         st.warning("Code execution only supported for Python")
#     elif st.session_state.history:
#         last_code = st.session_state.history[-1]["output"]

#         try:
#             exec_globals = {}
#             exec(last_code, exec_globals)
#             st.success("✅ Code executed successfully")
#         except Exception as e:
#             st.error(f"❌ Execution Error: {e}")
#     else:
#         st.warning("No code available to run")

# -----------------------------
# DISPLAY LATEST OUTPUT
# -----------------------------
if st.session_state.history:
    st.subheader("📌 Latest Output")
    latest = st.session_state.history[-1]
    code_lang = "python" if latest["language"] == "Python" else "sql"
    st.code(latest["output"], language=code_lang)

# -----------------------------
# CHAT HISTORY (BELOW)
# -----------------------------
st.subheader("📜 Chat History")

if not st.session_state.history:
    st.info("No history yet")
else:
    for i, item in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"Request {i}"):
            st.markdown(f"**Input:**\n{item['input']}")
            code_lang = "python" if item["language"] == "Python" else "sql"
            st.markdown("**Output:**")
            st.code(item["output"], language=code_lang)