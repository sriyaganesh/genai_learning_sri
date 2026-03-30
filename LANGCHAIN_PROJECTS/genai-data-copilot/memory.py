def format_history(history):
    return "\n".join([
        f"User: {q}\nAI: {a}" for q, a in history[-5:]
    ])