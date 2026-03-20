import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

from utils.vectorstore import create_vectorstore_from_docs

# Initialize LLM
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    temperature=0.5
)

# Conversation memory
conversation_history = []

# SerpAPI Key
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")


def web_search(query):
    """Search Google via SerpAPI and return top 5 snippets"""
    if not SERPAPI_KEY:
        return "SerpAPI key not configured."

    url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": SERPAPI_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return "Web search failed."

    results = response.json().get("organic_results", [])
    snippets = []
    for r in results:
        snippet = r.get("snippet") or r.get("title")
        if snippet:
            snippets.append(snippet)
    return "\n".join(snippets[:5]) if snippets else "No web results found."


def create_rag_agent(vectorstore=None, allow_web_search=True):
    """
    Returns a RAG agent function.
    
    Parameters:
    - vectorstore: optional pre-built vectorstore from uploaded documents
    - allow_web_search: if True, will search the web when vectorstore is missing or no relevant docs
    """

    rag_prompt = PromptTemplate(
        input_variables=["context", "history", "question"],
        template="""
        You are an AI assistant.

        Conversation History:
        {history}

        Context from documents or web:
        {context}

        Question:
        {question}

        Answer in a clear, concise manner:
        """
    )

    def query_rag(user_query):
        context = ""

        # Search vectorstore first if available
        if vectorstore:
            results = vectorstore.similarity_search(user_query, k=5)
            if results:
                context = " ".join([r.page_content for r in results])

        # Fallback to web search if allowed and no context found
        if not context.strip() and allow_web_search:
            context = web_search(user_query)

        # Build prompt with conversation history
        history_text = "\n".join(
            [f"User: {h['input']}\nAI: {h['output']}" for h in conversation_history]
        )

        # Get answer from LLM
        chain = rag_prompt | llm
        answer = chain.invoke({
            "context": context,
            "history": history_text,
            "question": user_query
        })

        # Update conversation memory
        conversation_history.append({"input": user_query, "output": answer.content})

        return answer.content

    return query_rag