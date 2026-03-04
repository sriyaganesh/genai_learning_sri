import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
# ---------------------------
# CONFIG
# ---------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


st.title("Closed LLM Assistant")

user_input = st.text_area("Ask something")

if st.button("Submit"):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful enterprise AI assistant."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.3
    )

    st.write(response.choices[0].message.content)