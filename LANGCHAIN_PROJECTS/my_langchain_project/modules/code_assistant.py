from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0)

code_prompt_template = PromptTemplate(
    input_variables=["task", "code", "language"],
    template="""
You are a coding assistant. Task: {task} 
Language: {language}
Code:{code}
Provide optimized and correct output.
"""
)

def code_assistant(task, code="", language="Python"):
    #chain = LLMChain(llm=llm, prompt=code_prompt_template)
    code_text = code if code else "N/A"
    chain = code_prompt_template | llm
    result = chain.invoke({"task": task, "code": code_text, "language": language})
    return result.content