import pandas as pd
from ...models import Stock, StockHistorical

opens = pd.read_csv("opening_prices.csv", index_col=0, parse_dates=True)
closes = pd.read_csv("closing_prices.csv", index_col=0, parse_dates=True)
print(open.head())