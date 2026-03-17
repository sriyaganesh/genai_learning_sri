import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


import os
from dotenv import load_dotenv
load_dotenv()
# Initialize LLM
llm=ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0.5)

# Initialize Prompt
prompt=PromptTemplate(
     input_variables=["code_task"],
    template="""
You are a professional coding assistant. Help the user with the following task. 
User says: {code_task}
Provide clean, well commented code and explanations if needed
"""
)

# LLM Chain creation
chain =  prompt | llm


# Streamlit UI


st.title("AI Coding Assistant")

coding_task=st.text_area("Describe the coding task to be done:")

if st.button("Generate Code"):
    if coding_task.strip() == "":
        st.warning("Please enter coding task description")
    else:
        response=chain.invoke({"code_task": coding_task})
        st.subheader("AI Assistant Response:")
        st.code(response.content,language='python', height=200)
            