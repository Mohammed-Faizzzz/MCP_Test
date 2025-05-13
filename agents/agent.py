import requests, random
from agents.llm_logic import llm_decision

class MCPAgent:
    def __init__(self, agent_id, task):
        self.id = agent_id
        self.task = task
        self.registry_url = "http://localhost:8000/tools/tag/" + task["tag"]

    def choose_tool(self):
        tools = requests.get(self.registry_url).json()
        random.shuffle(tools)  # simulate randomized UX
        return llm_decision(self.task, tools)
