import time
import csv
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_KEY")

def get_sp500_companies():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("table", {"id": "constituents"})
    companies = []
    for row in table.tbody.find_all("tr")[1:]:
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

def get_summary_from_gemini(ticker, name):
    prompt = f"Give me a summary of the company {name} (${ticker}), what they do, how they make money, and their future outlook in 3 sentences."
    print(prompt)
    if GEMINI_API_KEY:
        client = genai.Client(api_key=GEMINI_API_KEY)

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt

            )
            return response.text
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("GEMINI_KEY environment variable not set.")


def main():
    companies = get_sp500_companies()
    domains = {}
    summaries = {}
    for company in companies:
        ticker = company['ticker']
        name = company['name']
        domains[ticker] = get_company_domain(company['wiki_url'])
        summaries[ticker] = get_summary_from_gemini(ticker, name)
        # Optional: sleep between API calls to avoid rate limits.
        time.sleep(0.5)
    
    # Print dictionaries for debugging.
    print(domains)
    print(summaries)
    
    # Write the output to a CSV file.
    with open("sp500_summaries.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["ticker", "name", "domain", "summary"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for company in companies:
            ticker = company["ticker"]
            writer.writerow({
                "ticker": ticker,
                "name": company["name"],
                "domain": domains.get(ticker, ""),
                "summary": summaries.get(ticker, "")
            })
    print("CSV file generated: sp500_summaries.csv")


if __name__ == "__main__":
    main()