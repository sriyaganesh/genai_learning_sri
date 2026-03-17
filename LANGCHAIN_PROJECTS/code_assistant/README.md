# 💻 AI Coding Assistant

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-%E2%89%A53.20-orange)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT-4-purple)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A **Streamlit-based AI Coding Assistant** powered by **LangChain** and **OpenAI**.  
It helps developers **generate, explain, debug, and optimize code** in **Python, SQL, and Teradata** with a clean, user-friendly interface and chat history support.

---

## 🛠 Features

- **Multi-language support:** Python, SQL, Teradata  
- **Multiple modes:**  
  - Generate Code  
  - Explain Code  
  - Debug Code  
  - Optimize Code  
- **Live code execution:** Execute Python code directly in the app  
- **Chat history:** View all previous requests and AI responses  
- **Configurable AI model:** `gpt-4o` or `gpt-4o-mini`  
- **Clean, responsive UI** with Streamlit  
- **Lightweight & easily extendable** for advanced features like RAG or Agentic AI  

---

## 📌 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-coding-assistant.git
cd ai-coding-assistant

Create and activate a virtual environment

python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Set OpenAI API Key
Create a .env file in the root folder:

OPENAI_API_KEY=your_openai_api_key_here
🚀 Usage

Run the app:

streamlit run app.py
How to Use

Configure options (top panel)

Select Mode (Generate / Explain / Debug / Optimize)

Select Language (Python / SQL / Teradata)

Select Model (gpt-4o / gpt-4o-mini)

Enter your request or code snippet in the text area

Click Generate to get AI-generated output

Optionally click Run Code (Python Only) to execute the code

View latest output and scroll down to see full chat history

📂 Folder Structure
ai-coding-assistant/
├─ app.py              # Main Streamlit app
├─ requirements.txt    # Python dependencies
├─ README.md           # Project documentation
├─ .env                # Environment variables (OpenAI API Key)
⚡ Technologies Used

Python 3.10+

Streamlit – UI framework

LangChain – LLM orchestration

OpenAI API – GPT-4 based LLM

dotenv – Environment variable management
