import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "metrics/results.sqlite"  # Change if needed

# Load data
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM logs", conn)
conn.close()

# Error rate per task
task_error_rate = df.groupby("task_id")["is_legit"].apply(lambda x: 1 - x.mean()).reset_index(name="error_rate")

# Overall error rate
overall_error_rate = 1 - df["is_legit"].mean()

# Tool usage
tool_usage = df["tool_id"].value_counts().reset_index()
tool_usage.columns = ["tool_id", "count"]

# LLM instance error rate
instance_error_rate = df.groupby("ollama_instance")["is_legit"].apply(lambda x: 1 - x.mean()).reset_index(name="error_rate")

# 1. Error rate per task
task_error_rate["task_id"] = task_error_rate["task_id"].str.extract(r't(\d+)').astype(int)
task_error_rate = task_error_rate.sort_values("task_id")

plt.figure(figsize=(10, 5))
plt.bar("#" + task_error_rate["task_id"].astype(str), task_error_rate["error_rate"])
plt.title("Error Rate per Task")
plt.xlabel("Task ID")
plt.ylabel("Error Rate")
plt.xticks(rotation=45)
plt.tight_layout()
# plt.show()
plt.savefig("error_rate_per_task.pdf")

# 2. Overall error rate
plt.figure(figsize=(4, 4))
plt.bar(["Overall"], [overall_error_rate], color="red")
plt.title("Overall Impersonation Error Rate")
plt.ylim(0, 1)
plt.tight_layout()
# plt.show()
plt.savefig("overall_error_rate.pdf")

# 3. Tool usage frequency
plt.figure(figsize=(12, 6))
plt.bar(tool_usage["tool_id"], tool_usage["count"])
plt.title("Tool Usage Frequency")
plt.xlabel("Tool ID")
plt.ylabel("Selection Count")
plt.xticks(rotation=90)
plt.tight_layout()
# plt.show()
plt.savefig("tool_usage_frequency.pdf")

# 4. Error rate per LLM instance
plt.figure(figsize=(8, 4))
plt.bar(instance_error_rate["ollama_instance"], instance_error_rate["error_rate"], color="orange")
plt.title("Error Rate per LLM Instance")
plt.xlabel("LLM Instance")
plt.ylabel("Error Rate")
plt.ylim(0, 1)
plt.tight_layout()
# plt.show()
plt.savefig("error_rate_per_llm_instance.pdf")
