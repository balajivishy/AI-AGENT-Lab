import requests

def analyze_job(title):

    prompt = f"""
Extract from this internship title:

1. required skills
2. job category
3. difficulty (easy, medium, hard)

Return JSON.

Job: {title}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:mini",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]