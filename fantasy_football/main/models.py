from django.db import models
from django.contrib.auth.models import User

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
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_address = models.CharField(max_length=30)
    team_name = models.CharField(max_length=30)
    user_stocks = models.ManyToManyField('Stock', related_name="users")

class League(models.Model):
    weeks = models.IntegerField(max_digits=3)
    current_week = models.IntegerField(max_digits=3)

class Matchup(models.Model):
    league = models.ForeignKey('League', on_delete=models.CASCADE)
    week = models.IntegerField(max_digits=3)
    first_user = models.ForeignKey('UserProfile', related_name="matchups")
    second_user = models.ForeignKey('UserProfile', related_name="matchups")
    # 0 not finished, 1 first user won, 2 second user won, 3 tie
    winner = models.IntegerField(max_digits=1, default=0)

