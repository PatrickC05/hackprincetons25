import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("Please set the API_KEY environment variable in your .env file.")

# Define the endpoint and parameters for the API call
url = "https://newsapi.org/v2/everything"
params = {
    "q": "$PLTR",           # Query for articles related to $PLTR
    "sortBy": "publishedAt", # Sort articles by the most recent
    "language": "en",        # Limit to English articles
    "apiKey": api_key
}

# Make the API request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    articles = data.get("articles", [])
    # Print the title and URL for each article
    for article in articles:
        print(f"Title: {article['title']}\nURL: {article['url']}\n")
else:
    print("Failed to fetch articles:", response.status_code, response.text)