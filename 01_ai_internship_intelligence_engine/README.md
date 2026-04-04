# AI-Powered Internship Scraper 🚀

An end-to-end system that scrapes internship listings, enriches them using a local LLM (Ollama), and enables intelligent filtering based on skills and domains.

---

## 📌 Features

- 🔄 Concurrent Scraping Pipeline  
  Scrapes internship listings from Internshala using a structured pipeline.

- 🤖 AI Job Analysis (Local LLM)  
  Uses Ollama (phi3:mini) to extract:
  - required skills  
  - job category  
  - difficulty level  

- 🧠 Smart Filtering System  
  CLI-based filtering supporting:
  - single keyword (e.g., `python`)
  - multi-keyword queries (e.g., `python backend`)
  - domain-aware filtering (electronics, embedded, etc.)

- 💾 Structured Storage  
  Stores enriched job data in `jobs.json`.

---

## 🏗️ System Architecture

Internshala  
↓  
Scraper (BeautifulSoup)  
↓  
Structured Job Data  
↓  
AI Analyzer (Ollama)  
↓  
jobs.json  
↓  
Filter CLI (Python)  

---

## 🛠️ Tech Stack

- Python  
- BeautifulSoup (HTML parsing)  
- Requests / HTTPX (networking)  
- Asyncio (concurrency)  
- Ollama (local LLM)  

---

## 🚀 How to Run

1. Install dependencies

```bash
pip install requests beautifulsoup4 httpx

2. Start Ollama
 
Ollama run phi3:mini

3. Run scraper

python main.py

#This will:
scrape internships
run AI analysis
store results in jobs.json

4. Filter jobs

python filter_jobs.py python

python filter_jobs.py "python backend"


Example output:

Title: Software Development Intern  
Company: XYZ Pvt Ltd  
Source: Internshala  
  
