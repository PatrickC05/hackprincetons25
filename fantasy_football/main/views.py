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
    return render(request, 'matchup.html', {'user': user_profile, 'opponent': opponent})
