import json
import sys
import requests


def load_jobs():
    with open("jobs.json") as f:
        return json.load(f)


def analyze(text):

    prompt = f"""
You are a career assistant.

Analyze this internship:

{text}

Return:
1. Required skills
2. Role type
3. Difficulty
4. Short summary
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "tinyllama",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


def main():

    jobs = load_jobs()

    if len(sys.argv) < 2:
        print("Usage:")
        print("python analyze_on_demand.py <job index>")
        sys.exit()

    index = int(sys.argv[1])

    job = jobs[index]

    print("\n🔍 Job Selected:\n")
    print(job["title"], "-", job["company"])

    print("\n🤖 AI Analysis:\n")

    result = analyze(job["title"])
    print(result)


if __name__ == "__main__":
    main()