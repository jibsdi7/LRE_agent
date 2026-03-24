import ollama
import json
import re

def decide_steps(prompt):
    system_prompt = """
You are an automation agent.

Available tools:
1. login
2. open_report
3. extract_table

Return ONLY JSON like:
[
  {"tool": "login"},
  {"tool": "open_report"},
  {"tool": "extract_table"}
]
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    result = response["message"]["content"]

    print("🧠 Ollama Output:", result)

    # Clean JSON (important for local models)
    result = re.search(r"\[.*\]", result, re.DOTALL).group()

    return json.loads(result)