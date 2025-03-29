import yfinance as yf
import pandas as pd
import time

# Get the list of S&P 500 tickers from Wikipedia
sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
tables = pd.read_html(sp500_url, header=0)
sp500_table = tables[0]
tickers = sp500_table['Symbol'].tolist()
tickers = [ticker.replace('.', '-') for ticker in tickers]

# Define parameters
start_date = '2020-01-01'
batch_size = 50  # number of tickers per batch
delay = 3  # seconds to wait between batches

# Split tickers into batches
ticker_batches = [tickers[i:i + batch_size] for i in range(0, len(tickers), batch_size)]
data_frames = []

for batch in ticker_batches:
    try:
        print(f"Downloading data for batch: {batch}")
        data = yf.download(batch, start=start_date)
        data_frames.append(data)
    except Exception as e:
        print(f"Error downloading batch {batch}: {e}")
    time.sleep(delay)

# Combine data frames
combined_data = pd.concat(data_frames, axis=1)

# Extract opening and closing prices
opening_prices = combined_data['Open']
closing_prices = combined_data['Close']

# Save to CSV files
opening_prices.to_csv("opening_prices.csv")
closing_prices.to_csv("closing_prices.csv")