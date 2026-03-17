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
     input_variables=["key_points"],
    template="""
You are an expoert in email writer. Using the following bullet points draft a professional , friendly email
{key_points}
Make sure the email has greetings and clear structure
 and a closing"""
)

# LLM Chain creation
chain =  prompt | llm


# Streamlit UI


st.title("Smart Email Writer")

st.write("Enter Key Points for your email:")

key_points=st.text_area("Key Points")

if st.button("Generate Email"):
    if key_points.strip() == "":
        st.warning("Please enter Key points for your email")
    else:
        response=chain.invoke({"key_points": key_points})
        st.subheader("AI Assistant Drafted Email:")
        st.write(response.content)
            