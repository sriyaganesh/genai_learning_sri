from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4o-mini",
    temperature=0.3
)

def ask_llm(prompt):
    return llm.invoke(prompt).content