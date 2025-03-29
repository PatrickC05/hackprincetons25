"""
URL configuration for fantasy_football project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from .views import home, team, matchup, stock_detail, leaderboard, team_view

def custom_logout(request):
    logout(request)
    return redirect('home')  # Redirects to home page


urlpatterns = [
   path('', home, name='home'),
   path('team/', team, name='team'),
    path('team/<int:user_id>/', team_view, name='team_view'),  # View for other users' teams
   path('login/', LoginView.as_view(template_name='login.html'), name='login'),
   path('matchup/', matchup, name='matchup'),
   path('stocks/<str:ticker>/', stock_detail, name='stock_detail'),
   path('logout/', custom_logout, name='logout'),
   path('leaderboard/', leaderboard, name='leaderboard'),
]
