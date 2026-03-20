from langchain_core.prompts import PromptTemplate

LEARNING_PROMPT = PromptTemplate(
    input_variables=["topic", "mode", "user_answer"],
    template="""
You are a learning AI assistant.

Mode: {mode} (teach/quiz/evaluate)
Topic: {topic}
User Answer: {user_answer if user_answer else "N/A"}

Instructions:
- teach: Provide short summary bites for the topic
- quiz: Generate a question on the topic
- evaluate: Analyze user answer and provide feedback + improvement insights
"""
)