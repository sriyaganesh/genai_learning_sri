from langchain_core.prompts import PromptTemplate

CODE_PROMPT = PromptTemplate(
    input_variables=["task", "code", "language"],
    template="""
You are an expert coding assistant.

Task: {task}
Language: {language}
Code: {code if code else "N/A"}

Please provide the optimized, corrected, or explained version depending on the task.
"""
)