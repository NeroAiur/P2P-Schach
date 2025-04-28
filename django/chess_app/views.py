import sys
import os
import json
import hashlib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from backend.database_ops import add_user, get_uID, user_login
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


def index(request):
    return render(request, "index.html")

# PSEUDOCODE/IDEE
@csrf_exempt
def register_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    add_user("../db/user.db", username, password)
    uID = get_uID("../db/user.db", username, password)

    return redirect('dashboard', uID=uID)

@csrf_exempt
def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user_login("../db/user.db", username, password)
    uID = get_uID("../db/user.db", username, password)

    return redirect('dashboard', uID=uID)

def render_dashboard(request, uID):
    context = {
        'uID' : uID,
    }
    return render(request, "dashboard.html", context)

class GameView(TemplateView):
    template_name = "chessboard.html"

class DashboardView(TemplateView):
    template_name = "dashboard.html"


# class ProfileView(TemplateView):
#     template_name = "home.html"
#     add_user(dbpath, username, password)
#     return render(request, "base.html")

def get_move_to_game_calc(request):
    move = request.POST.post('move')

def send_move_to_game_calc(request):
    move = request.POST.post('move')
