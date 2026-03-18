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
     input_variables=["role", "JD"],
    template="""
You are a Senior Technical interviewer. 
Given this job role :{role}
and the Job Description: {JD}
Generate 5 **technical** mock interview questions for this role
Only include questions that test technical skills , knowledge and problem solving
DO NOT include sutuational or behavioural questions
For each question provide a stromg clear sample answer
Number 1 to 5 like this :
1. Question: ---
Answer:---
"""
)

# LLM Chain creation
chain =  prompt | llm


# Streamlit UI


st.title("Mock Interview Practice")

role=st.text_input("Enter Job Role:")
jd=st.text_area("Enter Job Description:")


if st.button("Generate Q&A"):
    if not role or not jd:
        st.warning("Please enter Job Role and Job Desfription")
    else:
        qa=chain.invoke({"role": role, "JD": jd})
        st.subheader("Mock Interview Q&A")
        st.code(qa.content)
            