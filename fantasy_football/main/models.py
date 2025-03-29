from django.db import models

# Create your models here.

class StockHistorical(models.Model):
    date = models.DateField()
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE, sorted=True)
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('date', 'open', 'close')

class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pe = models.DecimalField(max_digits=10, decimal_places=2)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2)
    sector = models.CharField(max_length=20)

    def __str__(self):
        return self.ticker