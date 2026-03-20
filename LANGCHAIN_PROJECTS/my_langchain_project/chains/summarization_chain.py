from langchain.chat_models import ChatOpenAI
from prompts.summarizer_prompt import SUMMARY_PROMPT
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0.5)

def get_summary(text):
    
    chain = SUMMARY_PROMPT | llm
    result = chain.invoke({"content": text})
    return result