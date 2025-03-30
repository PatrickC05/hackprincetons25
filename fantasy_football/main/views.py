from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import UserProfile, League, Matchup, Stock, StockHistorical
from django.urls import reverse_lazy
from django.db.models import Q, Count, Sum, Case, When, IntegerField, F
import os
import json
import pandas as pd
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .utils import recent_monday
import json
import requests

# Create your views here.
def home(request):
    return render(request, 'home.html')

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
    active_stocks = Stock.objects.filter(stockleagues__users=user_profile, stockleagues__active=True).distinct()
    bench_stocks = Stock.objects.filter(stockleagues__users=user_profile, stockleagues__active=False).distinct()
    sector_abbs = {'Communication Services': 'COM', 'Consumer Discretionary': 'DIS', 
                   'Consumer Staples': 'STP', 'Energy': 'ENE', 'Financials': 'FIN',
                   'Health Care': 'HC', 'Industrials': 'IND', 'Information Technology': "IT",
                   'Materials': 'MAT', 'Real Estate': 'RE', 'Utilities': 'UT'}
    sectors = ['Communication Services', 'Consumer Discretionary', 
                   'Consumer Staples', 'Energy', 'Financials',
                   'Health Care', 'Industrials', 'Information Technology',
                   'Materials', 'Real Estate', 'Utilities']
    sector_stocks = {}
    flex_stocks = []
    for stock in active_stocks:
        if len(sector_stocks) < 6 and stock.sector not in sector_stocks:
            sector_stocks[stock.sector] = stock
        elif len(flex_stocks) < 3:
            flex_stocks.append(stock)
    # for sector in sectors:
    #     if sector not in sector_stocks:
    #         sector_stocks[sector] = ''
    return render(request, 'team.html', {'user_profile': user_profile, 'sector_stocks': sector_stocks,
                                         'flex_stocks': flex_stocks,'sector_abbs': sector_abbs,
                                         'sectors': sectors,'bench_stocks':bench_stocks})
    # user_stocks = Stock.objects.filter(stockleague__users=user_profile).distinct()
    # return render(request, 'team.html', {'user_profile': user_profile, 'user_stocks': user_stocks,
    #                                      'sector_abbs': sector_abbs})

def team_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    if not user_profile.league:
        return HttpResponse("This user is not part of any league.")
    active_stocks = Stock.objects.filter(stockleagues__users=user_profile, stockleagues__active=True).distinct()
    bench_stocks = Stock.objects.filter(stockleagues__users=user_profile, stockleagues__active=False).distinct()
    sector_abbs = {'Communication Services': 'COM', 'Consumer Discretionary': 'DIS', 
                   'Consumer Staples': 'STP', 'Energy': 'ENE', 'Financials': 'FIN',
                   'Health Care': 'HC', 'Industrials': 'IND', 'Information Technology': "IT",
                   'Materials': 'MAT', 'Real Estate': 'RE', 'Utilities': 'UT'}
    sectors = ['Communication Services', 'Consumer Discretionary', 
                   'Consumer Staples', 'Energy', 'Financials',
                   'Health Care', 'Industrials', 'Information Technology',
                   'Materials', 'Real Estate', 'Utilities']
    sector_stocks = {}
    flex_stocks = []
    for stock in active_stocks:
        if len(sector_stocks) < 6 and stock.sector not in sector_stocks:
            sector_stocks[stock.sector] = stock
        elif len(flex_stocks) < 3:
            flex_stocks.append(stock)
    for sector in sectors:
        if sector not in sector_stocks:
            sector_stocks[stock.sector] = ''
    return render(request, 'team.html', {'user_profile': user_profile, 'sector_stocks': sector_stocks,
                                         'flex_stocks': flex_stocks,'sector_abbs': sector_abbs,
                                         'sectors': sectors,'bench_stocks':bench_stocks})

@login_required
def startsit(request):
    if request.method == "POST":
        print("HERE")
        body = json.loads(request.body) # Print the raw request body for debugging
        stock1 = get_object_or_404(Stock, ticker__iexact=body.get('ticker'))
        action = body.get('action')
        user_profile = request.user.userprofile
        active_stocks = Stock.objects.filter(stockleagues__users=user_profile, stockleagues__active=True)
        print(active_stocks)
        if action == 'start' and active_stocks.count() < 9:
            # Start the stock
            stock1.stockleagues.filter(users=request.user.userprofile, active=False).update(active=True)
            return JsonResponse({'success': True})  # Redirect to the team page after starting the stock
        elif action == 'sit':
            # Sit the stock
            stock1.stockleagues.filter(users=request.user.userprofile, active=True).update(active=False)
            return JsonResponse({'success': True})
        elif action == 'swap':
            stock2 = get_object_or_404(Stock, ticker__iexact=body.get('ticker2'))
            # Swap the stocks
            if stock1.stockleagues.filter(users=request.user.userprofile, active=True).exists() and stock2.stockleagues.filter(users=request.user.userprofile, active=False).exists():
                # Swap which is active and which is inactive, swap them
                stock1.stockleagues.filter(users=request.user.userprofile, active=True).update(active=False)
                stock2.stockleagues.filter(users=request.user.userprofile, active=False).update(active=True)
            return JsonResponse({'success': True})  # Redirect to the team page after swapping
        return JsonResponse({'success': False, 'message': 'Invalid action.'})
    else:
        # If the request is not POST, redirect to the team page
        return redirect('team')


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
    first_user_stocks = Stock.objects.filter(stockleagues__users=user_profile)
    second_user_stocks = Stock.objects.filter(stockleagues__users=opponent)
    first_active_stocks = Stock.objects.filter(stockleagues__users=user_profile, stockleagues__active=True)
    second_active_stocks = Stock.objects.filter(stockleagues__users=opponent, stockleagues__active=True)

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
        score = round(stock.get_score(monday), 2)
        stock_scores[stock.ticker] = score
        first_user_score += score
    for stock in first_user_flex:
        score = round(stock.get_score(monday), 2)
        stock_scores[stock.ticker] = score
        first_user_score += score

    second_user_score = 0
    for stock in second_user_sectors:
        score = round(stock.get_score(monday), 2)
        stock_scores[stock.ticker] = score
        second_user_score += score
        
    for stock in second_user_flex:
        score = round(stock.get_score(monday), 2)
        stock_scores[stock.ticker] = score
        second_user_score += score
    
    for stock in first_user_bench:
        stock_scores[stock.ticker] = round(stock.get_score(monday), 2) 

    for stock in second_user_bench:
        stock_scores[stock.ticker] = round(stock.get_score(monday), 2) 

    return render(request, 'matchup.html', {'team1name': user_profile.team_name, 
                                            'team1id': user_profile.id,
                                            'team2name': opponent.team_name, 
                                            'team2id': opponent.id,
                                            'team1score': first_user_score,
                                            'team2score': second_user_score,
                                            'first_user_sectors': first_user_sectors,
                                            'first_user_flex': first_user_flex,
                                            'first_user_bench': first_user_bench,
                                            'second_user_sectors': second_user_sectors,
                                            'second_user_flex': second_user_flex,
                                            'second_user_bench': second_user_bench,
                                            'sector_abbs': sector_abbs,
                                            'stock_scores': stock_scores})


def stock_detail(request, ticker):
    stock = get_object_or_404(Stock, ticker__iexact=ticker)

    # Retrieve stock info
    name = stock.name
    sector = stock.sector
    pe_ratio = stock.pe
    market_cap = stock.market_cap
    summary = stock.summary

    # --- News API Fetch ---
    url = "https://newsapi.org/v2/everything"
    api_key = os.getenv("API_KEY")  # Make sure you've set this in your environment
    # More direct query: e.g. "AMZN stock"
    params = {
        "q": f"{ticker} stock",  
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": api_key,
        "pageSize": 100
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        all_articles = data.get("articles", [])
        print(f"NewsAPI returned {len(all_articles)} articles for '{params['q']}'")
    except (requests.RequestException, ValueError) as e:
        print("Failed to fetch news:", e)
        all_articles = []

    # --- Post-filtering ---
    # We'll just search for the raw ticker in article text
    ticker_lower = ticker.lower()
    filtered_articles = []
    for article in all_articles:
        title = (article.get("title") or "").lower()
        description = (article.get("description") or "").lower()
        content = title + " " + description
        # If the raw ticker is in the content, consider it relevant
        if ticker_lower in content:
            filtered_articles.append(article)

    # Let's cap at 10
    articles = filtered_articles[:10]

    # --- Prepare historical chart data ---
    historical_prices = stock.historical_prices.order_by('date').values('date', 'open_price', 'close_price')
    chart_data_list = []
    for hp in historical_prices:
        chart_data_list.append({
            'date': hp['date'].isoformat(),        # Convert date to ISO string
            'open_price': float(hp['open_price']), # Convert Decimal to float
            'close_price': float(hp['close_price']),
        })
    chart_data_json = json.dumps(chart_data_list)

    context = {
        'ticker': stock.ticker,
        'name': name,
        'sector': sector,
        'pe_ratio': pe_ratio,
        'market_cap': market_cap,
        'summary': summary,
        'chart_data_json': chart_data_json,
        'articles': articles,
    }
    return render(request, 'stock_detail.html', context)

@login_required
def leaderboard(request):
    user_profile = request.user.userprofile
    if not user_profile.league:
        messages.error(request, "You are not part of any league.")
        return redirect('team')  # Redirect to the team page if not part of a league
    user_profiles = UserProfile.objects.filter(league=user_profile.league).annotate(
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


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        team_name = request.POST["team_name"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect("register")

        # Create user and user profile
        user = User.objects.create_user(username=username, email=email, password=password1)
        UserProfile.objects.create(user=user, team_name=team_name, email_address=email)

        # Log in the user automatically
        user = authenticate(username=username, password=password1)
        if user:
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")  # Change "home" to your actual homepage URL name

    return render(request, "register.html")

def minigame(request):
    return render(request, 'base.html')