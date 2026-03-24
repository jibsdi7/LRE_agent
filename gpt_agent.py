from openai import OpenAI
import json

client = OpenAI()

def decide_steps(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": """
You are an automation agent.

Available tools:
1. login
2. open_report
3. extract_table

Return ONLY a JSON array like:
[
  {"tool": "login"},
  {"tool": "open_report"},
  {"tool": "extract_table"}
]
"""
            },
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content

    print("🧠 Raw GPT output:", content)

    return json.loads(content)