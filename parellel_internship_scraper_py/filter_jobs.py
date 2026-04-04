import json
import sys


# 🔹 Define domain keyword expansions (smart filtering)
DOMAIN_KEYWORDS = {

    "python": [
        "python", "django", "flask", "pandas"
    ]
}


def expand_keywords(user_input):
    """
    Expands keywords like 'electronics' into related terms.
    """
    words = user_input.lower().split()

    expanded = []

    for word in words:
        if word in DOMAIN_KEYWORDS:
            expanded.extend(DOMAIN_KEYWORDS[word])
        else:
            expanded.append(word)

    return expanded


def filter_jobs(keywords):

    with open("jobs.json") as f:
        jobs = json.load(f)

    filtered = []

    for job in jobs:

        text = (
    job.get("title", "") + " " +
    " ".join(job.get("skills", []))
).lower()

        if any(keyword in text for keyword in keywords):
            filtered.append(job)

    return filtered


def display_jobs(jobs):

    print(f"\nFound {len(jobs)} matching jobs:\n")

    for job in jobs:
        print("----------------------------")
        print("Title:", job.get("title", "N/A"))
        print("Company:", job.get("company", "N/A"))
        print("Source:", job.get("source", "N/A"))
        print()


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python filter_jobs.py <keyword(s)>")
        print("Example: python filter_jobs.py python backend")
        sys.exit()

    user_input = " ".join(sys.argv[1:])

    keywords = expand_keywords(user_input)

    results = filter_jobs(keywords)

    display_jobs(results)