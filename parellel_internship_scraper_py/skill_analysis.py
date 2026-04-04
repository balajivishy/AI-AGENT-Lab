import json
from collections import Counter
import matplotlib.pyplot as plt


# 🔹 Define skill keywords
SKILLS = [
    "python", "sql", "machine learning", "excel",
    "java", "c++", "javascript", "data analysis",
    "communication", "react", "node", "django"
]


def load_jobs():
    with open("jobs.json") as f:
        return json.load(f)


def extract_skills(jobs):

    skill_counts = Counter()

    for job in jobs:

        text = (
            job.get("title", "") + " " +
            job.get("analysis", "")
        ).lower()

        for skill in SKILLS:
            if skill in text:
                skill_counts[skill] += 1

    return skill_counts


def print_top_skills(skill_counts, total_jobs):

    print("\n📊 Top Skills Across Internships:\n")

    for i, (skill, count) in enumerate(skill_counts.most_common(10), 1):
        print(f"{i}. {skill.title()} ({count})")

    print("\n🧠 Insights:\n")

    for skill, count in skill_counts.most_common(5):

        percentage = (count / total_jobs) * 100

        print(f"{skill.title()} appears in ~{int(percentage)}% of listings → high demand")


def recommend_skills(skill_counts):

    print("\n🎯 What You Should Learn:\n")

    top = skill_counts.most_common(5)

    for i, (skill, _) in enumerate(top, 1):
        print(f"{i}. {skill.title()}")


def plot_skills(skill_counts):

    skills = [k for k, _ in skill_counts.most_common(8)]
    counts = [v for _, v in skill_counts.most_common(8)]

    plt.figure()
    plt.bar(skills, counts)
    plt.xticks(rotation=45)
    plt.title("Top Skills in Internship Listings")
    plt.tight_layout()
    plt.show()


def main():

    jobs = load_jobs()

    total_jobs = len(jobs)

    skill_counts = extract_skills(jobs)

    print_top_skills(skill_counts, total_jobs)

    recommend_skills(skill_counts)

    plot_skills(skill_counts)


if __name__ == "__main__":
    main()