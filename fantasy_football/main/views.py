from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import UserProfile, League, Matchup, Stock, StockHistorical
from django.urls import reverse_lazy

# Create your views here.
def home(request):
    return render(request, 'base.html')

class CustomLoginView(LoginView):
    template_name = 'login.html' 
    redirect_authenticated_user = True 
    success_url = reverse_lazy('team')

@login_required
def team(request):
    user_profile = request.user.userprofile
    return render(request, 'team.html', {'user_profile': user_profile})

def matchup(request):
    user_profile = request.user.userprofile
    league = user_profile.league
    matchups = league.matchups.all
    opponent = None
    for matchup in matchups:
        if user_profile.team_name == matchup.first_user.team_name:
            opponent = matchup.second_user
        elif user_profile.team_name == matchup.second_user.team_name:
            opponent = matchup.first_user
    sectors = ['IT', 'FIN', 'HC', 'IND', 'ESS', 'DES', 'ENE', 'MAT']
    sector_count = 0
    first_user_sectors = []
    first_user_flex = []
    first_user_bench = []
    for stock in user_profile.active_stocks:
        if stock.sector in sectors and sector_count < 6:
            sector_count += 1
            first_user_sectors.append(stock)
        else:
            first_user_flex.append(stock)

    for stock in user_profile.user_stocks:
        if stock not in user_profile.active_stocks:
            first_user_bench.append(stock)
    sector_count = 0
    second_user_sectors = []
    second_user_flex = []
    second_user_bench = []
    for stock in user_profile.active_stocks:
        if stock.sector in sectors and sector_count < 6:
            sector_count += 1
            second_user_sectors.append(stock)
        else:
            second_user_flex.append(stock)

    for stock in user_profile.user_stocks:
        if stock not in user_profile.active_stocks:
            second_user_bench.append(stock)

    # TODO: add points to stock somehow?
    first_user_score = 0
    for stock in first_user_sectors:
        first_user_score += stock.score
    for stock in first_user_flex:
        first_user_score += stock.score

    second_user_score = 0
    for stock in second_user_sectors:
        second_user_score += stock.score
    for stock in second_user_flex:
        second_user_score += stock.score

    return render(request, 'matchup.html', {'team1name': user_profile.team_name, 
                                            'team2name': opponent.team_name, 
                                            'first_user_score': first_user_score,
                                            'second_user_score': second_user_score,
                                            'first_user_sectors': first_user_sectors,
                                            'first_user_flex': first_user_flex,
                                            'first_user_bench': first_user_bench,
                                            'second_user_sectors': first_user_sectors,
                                            'second_user_flex': first_user_flex,
                                            'second_user_bench': second_user_bench,})
