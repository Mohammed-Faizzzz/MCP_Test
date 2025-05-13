import subprocess
import json

def llm_decision(task, tool_options):
    tool_list = "\n".join(
        [f"{i+1}. {t['name']}: {t['description']}" for i, t in enumerate(tool_options)]
    )

    prompt = f"""
You are an autonomous agent trying to solve this task:
"{task['description']}"

Here are your available tools:
{tool_list}

Which tool would you use to solve the task? Respond ONLY with the tool name.
    """.strip()

    # Run via ollama CLI
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    output = result.stdout.decode().strip().lower()
    print(f"LLM output: {output}")
    for tool in tool_options:
        if tool["name"].lower() in output or tool["id"].lower() in output:
            return tool
    print(tool_options)
    
    return tool_options[0]  # fallback
