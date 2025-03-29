from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StockHistorical(models.Model):
    date = models.DateField()
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE, related_name='historical_prices')
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.stock.ticker} - {self.date.strftime('%Y-%m-%d')}"

class StockLeague(models.Model):
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    league = models.ForeignKey('League', on_delete=models.CASCADE, related_name='stocks')
    week = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.stock.ticker} in {self.league.name} for week {self.week}"
    
class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pe = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2)
    sector = models.CharField(max_length=20)

    def __str__(self):
        return self.ticker
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_address = models.CharField(max_length=30)
    team_name = models.CharField(max_length=30)
    user_stocks = models.ManyToManyField('StockLeague', related_name="users", blank=True)
    active_stocks = models.ManyToManyField('Stock', related_name="users", blank=True)
    league = models.ForeignKey('League', related_name="users", on_delete=models.CASCADE, null=True, blank=True)

class League(models.Model):
    weeks = models.IntegerField()
    current_week = models.IntegerField()
    name = models.CharField(max_length=30)
    start = models.DateField()

class Matchup(models.Model):
    league = models.ForeignKey('League', on_delete=models.CASCADE, related_name="matchups")
    week = models.IntegerField()
    first_user = models.ForeignKey('UserProfile', related_name="matchups_1", on_delete=models.CASCADE)
    second_user = models.ForeignKey('UserProfile', related_name="matchups_2", on_delete=models.CASCADE)
    # 0 not finished, 1 first user won, 2 second user won, 3 tie
    winner = models.IntegerField(default=0)

