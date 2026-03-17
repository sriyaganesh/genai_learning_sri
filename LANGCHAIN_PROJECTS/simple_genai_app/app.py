from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

llm=ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0.7)

prompt=PromptTemplate(
     input_variables=["user_input"],
    template="""
You are a helpful AI assistant. 
User says: {user_input}
Your Response: 
"""
)

# LLM Chain
chain =  prompt | llm

if __name__ == "__main__":
    user_input = input("Ask me anything: ")

    response = chain.invoke({
        "user_input": user_input
    })

    print("AI says:", response.content)

