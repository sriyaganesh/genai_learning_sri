from langchain.chat_models import ChatOpenAI
from prompts.learning_prompt import LEARNING_PROMPT
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0.5)

def run_learning_assistant(topic, mode="teach", user_answer=None):
    chain = LEARNING_PROMPT | llm
    return chain.invoke({"topic": topic, "mode": mode, "user_answer": user_answer})