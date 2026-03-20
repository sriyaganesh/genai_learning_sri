from langchain_core.prompts import PromptTemplate

SUMMARY_PROMPT = PromptTemplate(
    input_variables=["content"],
    template="""
You are an expert AI summarizer. Summarize the following content clearly and concisely:
{content}
"""
)