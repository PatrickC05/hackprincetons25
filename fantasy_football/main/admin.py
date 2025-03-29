from django.contrib import admin
from .models import Stock, UserProfile, League, Matchup, StockHistorical, StockLeague

# Register your models here.
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name', 'price', 'pe', 'market_cap', 'sector')
    search_fields = ('ticker', 'name')
    list_filter = ('sector',)
admin.site.register(UserProfile)
admin.site.register(League)
admin.site.register(Matchup)
admin.site.register(StockHistorical)
admin.site.register(StockLeague)