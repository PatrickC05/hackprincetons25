import pandas as pd
import yfinance as yf
import time

# 1. Get S&P 500 companies data from Wikipedia
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
tables = pd.read_html(url, header=0)
sp500_table = tables[0]

# Use the 'Symbol', 'Security' (name) and 'GICS Sector' columns.
# Adjust tickers if necessary (e.g., 'BRK.B' becomes 'BRK-B' for yfinance)
sp500_table['Ticker'] = sp500_table['Symbol'].apply(lambda x: x.replace('.', '-'))

# 2. Function to process a batch of tickers
def process_batch(batch_df):
    tickers = batch_df['Ticker'].tolist()
    # Create a yfinance Tickers object for the batch
    tickers_obj = yf.Tickers(" ".join(tickers))
    results = []
    
    for _, row in batch_df.iterrows():
        ticker = row['Ticker']
        name = row['Security']
        sector = row['GICS Sector']
        try:
            # Get info from the batch object for each ticker
            info = tickers_obj.tickers[ticker].info
            pe_ratio = info.get('trailingPE')
            market_cap = info.get('marketCap')
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            pe_ratio, market_cap = None, None
        results.append({
            "Ticker": ticker,
            "Name": name,
            "Sector": sector,
            "P/E Ratio": pe_ratio,
            "Market Cap": market_cap
        })
    return results

# 3. Process tickers in batches of 50
all_results = []
batch_size = 50
num_rows = len(sp500_table)
for start in range(0, num_rows, batch_size):
    batch_df = sp500_table.iloc[start:start+batch_size]
    print(f"Processing batch {start // batch_size + 1} ({start} to {start + batch_size})...")
    batch_results = process_batch(batch_df)
    all_results.extend(batch_results)
    # Pause between batches to avoid rate limiting (adjust delay as needed)
    time.sleep(10)

# 4. Create a DataFrame from the results and save it to CSV
df = pd.DataFrame(all_results)
df.to_csv("sp500_financials_batch.csv", index=False)