import requests
from bs4 import BeautifulSoup

def scrape_internshala():
    url = "https://internshala.com/internships/software-development-internship/"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for card in soup.select(".individual_internship"):

        title = (
            card.select_one(".job-title-href") or
            card.select_one("h3")
        )

        company = (
            card.select_one(".company-name") or
            card.select_one(".company_name")
        )

        if title and company:
            jobs.append({
                "title": title.text.strip(),
                "company": company.text.strip(),
                "source": "Internshala"
            })

    return jobs