from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import UserProfile, League, Matchup, Stock, StockHistorical
from django.urls import reverse_lazy
from django.db.models import Q, Count, Sum, Case, When, IntegerField, F
import os
import json
import pandas as pd
from django.conf import settings

from .utils import recent_monday

# Create your views here.
def home(request):
    return render(request, 'base.html')

class CustomLoginView(LoginView):
    template_name = 'login.html' 
    redirect_authenticated_user = True 
    success_url = reverse_lazy('team')

@login_required
def team(request):
    sector_abbs = {'Communication Services': 'COM', 'Consumer Discretionary': 'DIS', 
                   'Consumer Staples': 'STP', 'Energy': 'ENE', 'Financials': 'FIN',
                   'Health Care': 'HC', 'Industrials': 'IND', 'Information Technology': "IT",
                   'Materials': 'MAT', 'Real Estate': 'RE', 'Utilities': 'UT'}
    user_profile = request.user.userprofile
    user_stocks = Stock.objects.filter(stockleague__users=user_profile).distinct()
    return render(request, 'team.html', {'user_profile': user_profile, 'user_stocks': user_stocks,
                                         'sector_abbs': sector_abbs})

def matchup(request):
    stock_scores = {}
    sector_abbs = {'Communication Services': 'COM', 'Consumer Discretionary': 'DIS', 
                   'Consumer Staples': 'STP', 'Energy': 'ENE', 'Financials': 'FIN',
                   'Health Care': 'HC', 'Industrials': 'IND', 'Information Technology': "IT",
                   'Materials': 'MAT', 'Real Estate': 'RE', 'Utilities': 'UT'}
    user_profile = request.user.userprofile
    league = user_profile.league
    matchup = league.matchups.filter(week=league.current_week).filter(Q(first_user=user_profile) | Q(second_user=user_profile)).first()
    opponent = matchup.second_user if matchup.first_user == user_profile else matchup.first_user
    first_user_sectors = []
    first_user_flex = []
    first_user_bench = []
    used_sectors = []
    first_user_stocks = Stock.objects.filter(stockleague__users=user_profile)
    second_user_stocks = Stock.objects.filter(stockleague__users=opponent)
    first_active_stocks = Stock.objects.filter(stockleague__users=user_profile, stockleague__active=True)
    second_active_stocks = Stock.objects.filter(stockleague__users=opponent, stockleague__active=True)

    for stock in first_active_stocks:
        if stock.sector not in used_sectors and len(used_sectors) < 6:
            used_sectors.append(stock.sector)
            first_user_sectors.append(stock)
        else:
            first_user_flex.append(stock)

    for stock in first_user_stocks:
        if stock not in first_active_stocks:
            first_user_bench.append(stock)
    second_user_sectors = []
    second_user_flex = []
    second_user_bench = []
    used_sectors = []
    for stock in second_active_stocks:
        if stock.sector not in used_sectors and len(used_sectors) < 6:
            used_sectors.append(stock.sector)
            second_user_sectors.append(stock)
        else:
            second_user_flex.append(stock)

    for stock in second_user_stocks:
        if stock not in second_active_stocks:
            second_user_bench.append(stock)

    monday = recent_monday()
    first_user_score = 0
    for stock in first_user_sectors:
        score = stock.get_score(monday)
        stock_scores[stock] = score
        first_user_score += score
        print('firstuserscore',first_user_score)
    for stock in first_user_flex:
        score = stock.get_score(monday)
        stock_scores[stock] = score
        first_user_score += score

    second_user_score = 0
    for stock in second_user_sectors:
        score = stock.get_score(monday)
        stock_scores[stock] = score
        second_user_score += score
        
    for stock in second_user_flex:
        score = stock.get_score(monday)
        stock_scores[stock] = score
        second_user_score += score

    return render(request, 'matchup.html', {'team1name': user_profile.team_name, 
                                            'team2name': opponent.team_name, 
                                            'team1score': first_user_score,
                                            'team2score': second_user_score,
                                            'first_user_sectors': first_user_sectors,
                                            'first_user_flex': first_user_flex,
                                            'first_user_bench': first_user_bench,
                                            'second_user_sectors': first_user_sectors,
                                            'second_user_flex': first_user_flex,
                                            'second_user_bench': second_user_bench,
                                            'sector_abbs': sector_abbs,
                                            'stock_scores': stock_scores})


def stock_detail(request, ticker):
    stock = get_object_or_404(Stock, ticker__iexact=ticker)
    
    name = stock.name
    sector = stock.sector
    pe_ratio = stock.pe
    market_cap = stock.market_cap
    summary = getattr(stock, 'summary', "No summary available.")
    
    # Retrieve historical prices as dictionaries.
    historical_prices = stock.historical_prices.order_by('date').values('date', 'open_price', 'close_price')
    chart_data_list = []
    for hp in historical_prices:
        chart_data_list.append({
            'date': hp['date'].isoformat(),       # Convert date to ISO string
            'open_price': float(hp['open_price']),  # Convert Decimal to float
            'close_price': float(hp['close_price']),
        })
    
    # Convert the list to a JSON string.
    chart_data_json = json.dumps(chart_data_list)
    
    news_articles = []
    
    context = {
        'ticker': stock.ticker,
        'name': name,
        'sector': sector,
        'pe_ratio': pe_ratio,
        'market_cap': market_cap,
        'summary': summary,
        'chart_data_json': chart_data_json,  # Pass JSON string, not the raw list.
        'articles': news_articles,
    }
    return render(request, 'stock_detail.html', context)


def leaderboard(request):
    user_profiles = UserProfile.objects.annotate(
        win_count=Count(
            Case(
                When(matchups_1__first_points__gt=F('matchups_1__second_points'), then=1),
                When(matchups_2__second_points__gt=F('matchups_2__first_points'), then=1),
                output_field=IntegerField(),
            )
        ),
        loss_count=Count(
            Case(
                When(matchups_1__first_points__lt=F('matchups_1__second_points'), then=1),
                When(matchups_2__second_points__lt=F('matchups_2__first_points'), then=1),
                output_field=IntegerField(),
            )
        ),
        total_points=(
            Sum('matchups_1__first_points', default=0) + Sum('matchups_2__second_points', default=0)
        )
    ).order_by('-win_count', '-total_points')

    return render(request, 'leaderboard.html', {'user_profiles': user_profiles})