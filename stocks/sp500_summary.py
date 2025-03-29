import os
import time
import csv
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
GEMINI_API = os.getenv("GEMINI_API")  # e.g., "https://api.gemini.com/v1/summarize"

def get_sp500_companies():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("table", {"id": "constituents"})
    companies = []
    for row in table.tbody.find_all("tr")[1:]:  # skip header
        cells = row.find_all("td")
        if len(cells) < 2:
            continue
        ticker = cells[0].get_text(strip=True)
        security_cell = cells[1]
        security_link = security_cell.find("a")
        security_name = security_link.get_text(strip=True) if security_link else security_cell.get_text(strip=True)
        wiki_url = "https://en.wikipedia.org" + security_link['href'] if security_link and security_link.has_attr('href') else None
        companies.append({
            "ticker": ticker,
            "name": security_name,
            "wiki_url": wiki_url,
        })
    return companies

def get_company_domain(wiki_url):
    if not wiki_url:
        return None
    try:
        response = requests.get(wiki_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        infobox = soup.find("table", {"class": "infobox"})
        if not infobox:
            return None
        for tr in infobox.find_all("tr"):
            header = tr.find("th")
            if header and "website" in header.get_text(strip=True).lower():
                link = tr.find("a", class_="external text")
                if link and link.has_attr("href"):
                    url = link['href']
                    domain = url.split("//")[-1].split("/")[0]
                    return domain
    except Exception as e:
        print(f"Error retrieving domain from {wiki_url}: {e}")
    return None

def get_summary_from_gemini(ticker, name, domain):
    prompt = f"Provide a concise summary for the company {name} (ticker: {ticker}). Official website: {domain if domain else 'N/A'}."
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "max_tokens": 150
    }
    try:
        response = requests.post(GEMINI_API, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        summary = data.get("summary", "No summary returned.")
        return summary
    except Exception as e:
        print(f"Error summarizing {ticker}: {e}")
        return "Error
