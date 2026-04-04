import json

from scraper.internshala import scrape_internshala
from utils.extract import extract_features


def main():

    print("Scraping Internshala...")
    jobs = scrape_internshala()

    print("Jobs collected:", len(jobs))

    print("Running logic-based extraction...")

    for job in jobs:

        features = extract_features(job)

        job["skills"] = features["skills"]
        job["category"] = features["category"]

    with open("jobs.json", "w") as f:
        json.dump(jobs, f, indent=2)

    print("Saved to jobs.json")


if __name__ == "__main__":
    main()