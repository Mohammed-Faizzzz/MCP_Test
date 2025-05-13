import sqlite3

conn = sqlite3.connect("metrics/results.sqlite")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS logs
             (agent_id INT, task_id TEXT, tool_id TEXT)''')

def log_result(agent_id, task_id, tool_id):
    c.execute("INSERT INTO logs VALUES (?, ?, ?)", (agent_id, task_id, tool_id))
    conn.commit()
