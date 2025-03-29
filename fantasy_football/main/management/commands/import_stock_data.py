import pandas as pd
from django.core.management.base import BaseCommand
from ...models import Stock, StockHistorical

class Command(BaseCommand):
    help = 'Imports stock data from CSV files into the database'

    def handle(self, *args, **kwargs):
        # Load the opening and closing prices
        opens = pd.read_csv("../stocks/opening_prices.csv", index_col=0, parse_dates=True)
        closes = pd.read_csv("../stocks/closing_prices.csv", index_col=0, parse_dates=True)
        info = pd.read_csv("../stocks/sp500_financials_batch.csv", index_col='Ticker')

        # Iterate through each stock and update the database
        for ticker in opens.columns:
            print(ticker)
            last_price = closes.at[closes.index[-1], ticker] if ticker in closes.columns else None
            name, sector, pe, market_cap = info.loc[ticker, ['Name', 'Sector', 'P/E Ratio', 'Market Cap']] if ticker in info.index else (None, None, None, None)
            pe, market_cap = float(pe) if pe is not None and pd.notna(pe) else None, float(market_cap) if market_cap is not None and pd.notna(market_cap) else None
            stock = Stock.objects.get(ticker=ticker) if ticker in Stock.objects.values_list('ticker', flat=True) else None
            if stock is None:
                stock = Stock.objects.create(ticker=ticker, price=last_price, name=name, sector=sector, pe=pe, market_cap=market_cap)
                self.stdout.write(self.style.SUCCESS(f'Created new stock: {ticker}'))
            # else:
            #     self.stdout.write(self.style.WARNING(f'Stock already exists: {ticker}'))

            # Update the stock's opening and closing prices
            for date in opens.index:
                try:
                    opening_price = opens.at[date, ticker]
                    closing_price = closes.at[date, ticker]
                    if pd.isna(opening_price) or pd.isna(closing_price):
                        continue
                    StockHistorical.objects.update_or_create(
                        stock=stock,
                        date=date,
                        defaults={'open_price': opening_price, 'close_price': closing_price}
                    )
                except KeyError:
                    self.stdout.write(self.style.ERROR(f'Missing data for {ticker} on {date}'))

        self.stdout.write(self.style.SUCCESS('Stock data import completed.'))