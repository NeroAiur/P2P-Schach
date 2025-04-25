import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from django.shortcuts import render
from django.views.generic.base import TemplateView
from backend.database_ops import add_user


def index(request):
    return render(request, "index.html")

# PSEUDOCODE/IDEE
# def send_login_data_to_login_function(request):
#     username = request.GET.get('username')
#     password = request.GET.get('password')

#     # nicht ganz sicher, was dbpath ist
#     add_user("db/user.db", username, password)
#     return render(request, "base.html")

class GameView(TemplateView):
    template_name = "game.html"

class ScoreboardView(TemplateView):
    template_name = "scoreboard.html"

# class ProfileView(TemplateView):
#     template_name = "home.html"
#     add_user(dbpath, username, password)
#     return render(request, "base.html")

def get_move_to_game_calc(request):
    move = request.POST.post('move')

def send_move_to_game_calc(request):
    move = request.POST.post('move')
