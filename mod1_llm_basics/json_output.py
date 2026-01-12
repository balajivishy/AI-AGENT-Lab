from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "user",
            "content": "Return three facts about AI in JSON format."
        }
    ]
)

print(response.choices[0].message.content)
