from langchain.chat_models import ChatOpenAI
from prompts.code_prompt import CODE_PROMPT
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0)

def run_code_assistant(task, code="", language="Python"):
    chain= CODE_PROMPT | llm
    return chain.invoke({"task": task, "code": code, "language": language})