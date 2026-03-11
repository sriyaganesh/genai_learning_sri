from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

print("Chatbot started. Type 'exit' to stop.\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chatbot ended.")
        break

    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=user_input)
    ]

    response = llm.invoke(messages)

    print("Bot:", response.content)