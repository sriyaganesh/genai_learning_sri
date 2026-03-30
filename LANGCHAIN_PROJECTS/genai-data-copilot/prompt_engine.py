def build_prompt(task, user_input, rag, schema, relationships, history, data_context=""):

    base = f"""
You are an expert Data Copilot.

Conversation:
{history}

Schema:
{schema}

Graph Relationships:
{relationships}

Data Insights:
{data_context}

Context:
{rag}

User Request:
{user_input}
"""

    task_map = {

        "🛠️ Design ETL": """
Design ETL:
- Identify fact & dimension tables
- Use relationships for joins
- Generate ETL SQL + PySpark
- Add data quality checks
""",

        "🧾 Write SQL": """
Generate SQL:
- Use relationships for joins
- Optimize query
- Explain logic
""",

        "🔍 Analyze pipeline": """
Analyze pipeline:
- Use relationships to detect missing joins
- Suggest improvements
""",

        "📊 Suggest dashboard": """
Provide:
- KPIs
- Drill-down paths using relationships
- Charts
""",

        "📄 Explain this document": """
Explain clearly with insights
""",

        "📈 Generate insights": """
Provide trends + insights from data
""",

        "🧪 Data quality checks": """
Generate validation rules
"""
    }

    return base + task_map.get(task, "")