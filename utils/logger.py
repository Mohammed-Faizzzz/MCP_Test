import sqlite3

conn = sqlite3.connect("metrics/results.sqlite")
c = conn.cursor()
c.execute("""
CREATE TABLE logs (
    agent_id INTEGER,
    task_id TEXT,
    tool_id TEXT,
    is_legit INTEGER,
    ollama_instance TEXT
)
""")

def log_result(agent_id, task_id, tool_id, is_legit, ollama_instance):
    c.execute(
        "INSERT INTO logs VALUES (?, ?, ?, ?, ?)",
        (agent_id, task_id, tool_id, is_legit, ollama_instance)
    )
    conn.commit()
