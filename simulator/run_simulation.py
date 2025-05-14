import json, random
from agents.agent import MCPAgent
from utils.logger import log_result
import requests

NUM_AGENTS = 100

with open("tasks/tasks.json") as f:
    tasks = json.load(f)

# Load registry
tools = requests.get("http://localhost:8000/tools").json()

with open("registry/tools/legit_tools.json") as f:
    legit_tools = json.load(f)
LEGIT_TOOL_IDS = {tool["id"] for tool in legit_tools}

# Validate tag coverage
tags_used = {task["tag"] for task in tasks}
tags_available = {tag for tool in tools for tag in tool["tags"]}
missing = tags_used - tags_available

if missing:
    print("ERROR: These task tags are missing from your tool registry:", missing)
    exit(1)
else:
    print("All task tags have matching tools.")


for i in range(NUM_AGENTS):
    task = random.choice(tasks)
    agent = MCPAgent(i, task)
    chosen_tool = agent.choose_tool()
    
    is_legit = 1 if chosen_tool["id"] in LEGIT_TOOL_IDS else 0
    
    ollama_instance = f"ollama-{i % 5}"
    
    log_result(agent.id, task["task_id"], chosen_tool["id"], is_legit, ollama_instance)

