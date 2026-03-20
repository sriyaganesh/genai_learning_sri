import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from utils.vectorstore import create_vectorstore_from_docs

load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    temperature=0
)

# Manual conversation memory
conversation_history = []

def create_rag_agent(vectorstore):
    """
    Creates a RAG agent that retrieves documents from the vectorstore
    and answers queries using ChatOpenAI. Memory is handled manually.
    """

    retriever = vectorstore.as_retriever()

    def query_rag(user_query):
        # 1️⃣ Retrieve relevant documents
        results = retriever.get_relevant_documents(user_query)
        context = " ".join([r.page_content for r in results])

        # 2️⃣ Prepare conversation history
        history_text = "\n".join(
            [f"User: {h['input']}\nAI: {h['output']}" for h in conversation_history]
        )

        # 3️⃣ Build prompt
        prompt = f"""
You are an AI assistant.
Conversation history: {history_text}
Context from documents: {context}
Question: {user_query}
Answer:
"""

        # 4️⃣ Get answer from LLM
        answer = llm(prompt)

        # 5️⃣ Update memory
        conversation_history.append({"input": user_query, "output": answer})

        return answer

    return query_rag

# Example usage:
# vectorstore = create_vectorstore_from_docs(docs)
# rag_agent = create_rag_agent(vectorstore)
# answer = rag_agent("Explain the key points of the uploaded documents")
# print(answer)