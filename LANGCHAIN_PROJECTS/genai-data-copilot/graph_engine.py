from neo4j import GraphDatabase
from config import *

class GraphEngine:

    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD)
        )

    # -----------------------------
    # LOAD SCHEMA + RELATIONSHIPS
    # -----------------------------
    def load_schema(self, df):

        with self.driver.session() as session:

            # Create column nodes
            for col in df.columns:
                session.run(
                    "MERGE (c:Column {name:$name})",
                    name=col
                )

            # 🔥 AUTO RELATIONSHIP DETECTION
            columns = list(df.columns)

            for col in columns:
                if "_id" in col:
                    base = col.replace("_id", "")

                    for other in columns:
                        if base in other and col != other:
                            session.run("""
                            MATCH (a:Column {name:$a}),
                                  (b:Column {name:$b})
                            MERGE (a)-[:RELATES_TO]->(b)
                            """, a=col, b=other)

    # -----------------------------
    # GET SCHEMA
    # -----------------------------
    def get_schema(self):
        with self.driver.session() as session:
            result = session.run("MATCH (c:Column) RETURN c.name")
            return [r["c.name"] for r in result]

    # -----------------------------
    # GET RELATIONSHIPS
    # -----------------------------
    def get_relationships(self):
        with self.driver.session() as session:
            result = session.run("""
            MATCH (a)-[r]->(b)
            RETURN a.name AS source, type(r) AS rel, b.name AS target
            """)

            return [
                f"{r['source']} -> {r['target']}"
                for r in result
            ]