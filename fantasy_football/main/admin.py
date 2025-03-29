from django.contrib import admin
from .models import Stock, UserProfile, League, Matchup, StockHistorical

# Register your models here.
admin.site.register(Stock)
admin.site.register(UserProfile)
admin.site.register(League)
admin.site.register(Matchup)
admin.site.register(StockHistorical)