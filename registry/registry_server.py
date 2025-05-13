import os
import json
from fastapi import FastAPI

app = FastAPI()

BASE_DIR = os.path.dirname(__file__)
LEGIT_TOOLS_PATH = os.path.join(BASE_DIR, "tools", "legit_tools.json")
FAKE_TOOLS_PATH = os.path.join(BASE_DIR, "tools", "fake_tools.json")

with open(LEGIT_TOOLS_PATH) as f1, open(FAKE_TOOLS_PATH) as f2:
    tools = json.load(f1) + json.load(f2)

@app.get("/tools")
def get_tools():
    return tools

@app.get("/tools/tag/{tag}")
def get_tools_by_tag(tag: str):
    return [tool for tool in tools if tag in tool["tags"]]
