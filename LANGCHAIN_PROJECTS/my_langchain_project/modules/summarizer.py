from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0.5)

summary_prompt = PromptTemplate(
    input_variables=["content"],
    template="""
You are an expert summarizer. Summarize the following content concisely:
{content}
"""
)

def summarize_text(text):
    #chain = LLMChain(llm=llm, prompt=summary_prompt)
    chain= summary_prompt | llm
    result = chain.invoke({"content": text})
    return result.content