import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import PyPDF2


import os
from dotenv import load_dotenv
load_dotenv()
# Initialize LLM
llm=ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0.3)

# Initialize Prompt

prompt=PromptTemplate(
     input_variables=["resume_text","job_title","company"],
    template="""
You are an expert Career coach and content writer. 
Write a professional , personalized cover letter for thsis role
Job Titile: {job_title}
Company: {company}
Use the following resume for information:
{resume_text}
Keep the tone formal but friendly. Highlight relevant experience and enthusiasm for the role.
"""
)

# LLM Chain creation
chain =  prompt | llm


# Streamlit UI


st.title("Cover Letter Generator")

resume_file=st.file_uploader("Upload your Resume (PDF or TXT)", type=["pdf","txt","docx"])
job_title=st.text_input("Enter the Job Title (Ex: S/W Engineer):")
company=st.text_input("Company Name (optional):")

if st.button("Generate Cover Letter"):
    if not resume_file or not job_title:
        st.warning("Please upload your resume and enter Job Title")
    else:
        if resume_file.name.endswith(".txt"):
            resume_text=resume_file.load().decode("utf-8")
    
        elif resume_file.name.endswith(".pdf"):

            pdf_reader=PyPDF2.PdfReader(resume_file)
            resume_content=""
            for page in pdf_reader.pages:
                resume_content+=page.extract_text()

        else:
            st.error("Unsupported file format")

        if resume_content:
            cover_letter=chain.invoke({"resume_text": resume_content,
                                       "job_title": job_title
                                       ,"company": company if company else "The Company"
                                       
                                       })

        st.subheader("Generated Cover Letter:")
        st.write(cover_letter.content)
            