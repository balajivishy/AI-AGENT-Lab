from openai import OpenAI
client = OpenAI()

def get_weather(city: str):
    return {"temperature": 29, "condition": "Sunny"}

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What's the weather in Bangalore?"}],
    functions=[
        {
            "name": "get_weather",
            "description": "Get weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    ]
)
print(response.choices[0].message)