from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0.5)

learning_prompt = PromptTemplate(
    input_variables=["topic", "user_answer", "mode"],
    template="""
You are a learning assistant.
Mode: {mode} (teach/quiz/evaluate)
Topic: {topic}
User Answer: {user_answer}

- If teach: provide short summary bites
- If quiz: generate a question
- If evaluate: analyze user answer and give insights

"""
)

def learning_assistant(topic, mode="teach", user_answer=None):
    #schain = LLMChain(llm=llm, prompt=learning_prompt)
    user_answer_text=user_answer if user_answer else "N/A"
    chain=learning_prompt | llm
    result = chain.invoke({"topic": topic, "mode": mode, "user_answer": user_answer_text})
    return result.content