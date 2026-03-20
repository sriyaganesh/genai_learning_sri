import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

# Initialize LLM once per module
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    temperature=0.5
)

# Define prompt template
learning_prompt = PromptTemplate(
    input_variables=["topic", "user_answer", "mode", "docs"],
    template="""
You are a learning assistant.

Mode: {mode} (teach/quiz/evaluate)
Topic: {topic}

Uploaded Document (if any):
{docs}

User Answer (for evaluate mode):
{user_answer}

Instructions:
- If mode is 'teach': provide short summary bites.
- If mode is 'quiz': generate a question related to the topic or document.
- If mode is 'evaluate': analyze the user's answer and give insights.
"""
)


# Dedicated prompt for quiz question generation
quiz_prompt = PromptTemplate(
    input_variables=["topic", "docs", "num_questions"],
    template="""
You are a learning assistant.

Mode: quiz
Topic: {topic}

Uploaded Document (if any):
{docs}

Please generate {num_questions} clear and concise quiz questions based on the topic and/or the document.
Format the questions as a numbered list, with one question per line, e.g.:

1. What is...?
2. How does...?
3. Explain...

Only output the questions, no additional text.
"""
)

# Create a reusable function to invoke the chain
def learning_assistant(topic="", mode="teach", user_answer=None, docs=None):
    user_answer_text = user_answer if user_answer else "N/A"
    docs_text = docs if docs else "N/A"
    topic_text = topic if topic else "N/A"

    # Compose the chain inline
    chain = learning_prompt | llm
    response = chain.invoke({
        "topic": topic_text,
        "mode": mode,
        "user_answer": user_answer_text,
        "docs": docs_text,
    })

    return response.content



def generate_quiz_questions(topic="", docs=None, num_questions=10):
    """
    Generate a list of quiz questions based on topic or document.
    Returns a list of strings.
    """
    chain = quiz_prompt | llm
    response = chain.invoke({
        "topic": topic or "N/A",
        "docs": docs or "N/A",
        "num_questions": num_questions
    })

    content = response.content.strip()
    questions = []

    # Parse numbered questions (1. question)
    for line in content.splitlines():
        line = line.strip()
        if line and line[0].isdigit() and line[1:3] == ". ":
            q_text = line[3:].strip()
            if q_text:
                questions.append(q_text)

    # Fallback: split by newline if no numbered questions
    if not questions:
        questions = [q.strip() for q in content.split("\n") if q.strip()]

    return questions[:num_questions]



def generate_mcq_quiz(topic="", docs=None, num_questions=10):
    """
    Generate MCQs using ChatOpenAI.invoke.
    Returns a list of dicts: {"question": str, "options": [A,B,C,D], "answer": "A"}
    """

    docs_text = docs if docs else "No document provided."
    topic_text = topic if topic else "General knowledge"

    # Fill the prompt string manually
    prompt_text = f"""
You are an expert learning assistant.

Topic: {topic_text}
Document content (if any):
{docs_text}

Please generate {num_questions} multiple-choice questions (MCQs) to test knowledge on the topic.
- Each question must have exactly 4 options: A, B, C, D
- Clearly indicate the correct answer with 'Answer: X' (X = A/B/C/D)
- Format example:

Question: What is photosynthesis?
A. Process by which plants make food
B. Process of respiration
C. Process of decomposition
D. Process of evaporation
Answer: A

Output only the questions in the above format.
"""

    # ✅ Pass plain string to invoke
    response = llm.invoke(prompt_text)
    text = response.content.strip()

    # Parse MCQs
    mcqs = []
    current_q = None
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith("question:"):
            if current_q:
                # Ensure options and answer exist
                if "options" not in current_q or not current_q["options"]:
                    current_q["options"] = ["N/A"] * 4
                if "answer" not in current_q or not current_q["answer"]:
                    current_q["answer"] = "N/A"
                mcqs.append(current_q)
            current_q = {"question": line[9:].strip(), "options": [], "answer": ""}
        elif line.startswith(("A.", "B.", "C.", "D.")) and current_q:
            current_q["options"].append(line[2:].strip())
        elif line.lower().startswith("answer:") and current_q:
            current_q["answer"] = line[7:].strip().upper()
    if current_q:
        if "options" not in current_q or not current_q["options"]:
            current_q["options"] = ["N/A"] * 4
        if "answer" not in current_q or not current_q["answer"]:
            current_q["answer"] = "N/A"
        mcqs.append(current_q)

    return mcqs[:num_questions]