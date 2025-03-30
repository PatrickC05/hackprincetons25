import pandas as pd
from django.core.management.base import BaseCommand
from ...models import Stock

class Command(BaseCommand):
    help = 'Imports stock summaries from CSV files into the database'

    def handle(self, *args, **kwargs):
        # Load the summaries
        df = pd.read_csv('../stocks/sp500_summaries.csv')
        summaries_dict = df.set_index('ticker')['summary'].to_dict()

        # Iterate through each stock and update the database
        for ticker, summary in summaries_dict.items():
            try:
                stock = Stock.objects.get(ticker=ticker)
                stock.summary = summary
                stock.save()
                self.stdout.write(self.style.SUCCESS(f'Updated summary for stock: {ticker}'))
            except Stock.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Stock not found: {ticker}'))

        self.stdout.write(self.style.SUCCESS('Stock summaries import completed.'))