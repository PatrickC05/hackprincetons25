from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class StockHistorical(models.Model):
    date = models.DateField()
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE, related_name='historical_prices')
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.stock.ticker} - {self.date.strftime('%Y-%m-%d')}"

class StockLeague(models.Model):
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE, related_name='stockleagues')
    league = models.ForeignKey('League', on_delete=models.CASCADE, related_name='stocks')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.stock.ticker} in {self.league.name}"
    
class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pe = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2)
    sector = models.CharField(max_length=50)
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.ticker
    
    def get_score(self, monday):
        try:
            start_price = self.historical_prices.get(date=monday).open_price
            end_price = self.historical_prices.get(date=monday + datetime.timedelta(days=4)).close_price
            return ((end_price - start_price) / start_price) * 100
        except StockHistorical.DoesNotExist:
            return None
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_address = models.CharField(max_length=30)
    team_name = models.CharField(max_length=30)
    user_stocks = models.ManyToManyField('StockLeague', related_name="users", blank=True)
    league = models.ForeignKey('League', related_name="users", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.team_name} ({self.user.username})"

class League(models.Model):
    weeks = models.IntegerField()
    current_week = models.IntegerField()
    name = models.CharField(max_length=30)
    start = models.DateField()

    def __str__(self):
        return self.name

class Matchup(models.Model):
    league = models.ForeignKey('League', on_delete=models.CASCADE, related_name="matchups")
    week = models.IntegerField()
    first_user = models.ForeignKey('UserProfile', related_name="matchups_1", on_delete=models.CASCADE)
    second_user = models.ForeignKey('UserProfile', related_name="matchups_2", on_delete=models.CASCADE)
    # 0 not finished, 1 first user won, 2 second user won, 3 tie
    first_points = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    second_points = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    in_progress = models.BooleanField(default=True)

    def __str__(self):
        return f"Matchup: {self.first_user.team_name} vs {self.second_user.team_name} in {self.league.name} (Week {self.week})"