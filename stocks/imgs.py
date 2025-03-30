import pandas as pd
import urllib3
import os

df = pd.read_csv('sp500_summaries.csv')
urls_dict = df.set_index('ticker')['domain'].to_dict()

for ticker, domain in urls_dict.items():
    img_url = "https://logo.clearbit.com/" + domain
    print(f"Ticker: {ticker}, Image URL: {img_url}")
    # Here you can add code to download the image or process it further
    # For example, to download the image:
    http = urllib3.PoolManager()
    response = http.request('GET', img_url)
    if response.status == 200:
        with open(f'../fantasy_football/main/static/imgs/logos/{ticker}.png', 'wb') as img_file:
            img_file.write(response.data)
    else:
        print(f"Failed to retrieve image for {ticker}. Status code: {response.status}")