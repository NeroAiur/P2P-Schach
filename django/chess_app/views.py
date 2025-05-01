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
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

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

@csrf_exempt
def render_dashboard(request, uID):
    context = {
        'uID' : uID,
    }
    return render(request, "dashboard.html", context)

@csrf_exempt
def render_game(request, roomID):
    context = {
        'roomID' : roomID,
    }
    return render(request, "chessboard.html", context)

room_states = {}

@csrf_exempt
def join_game_room(request):
    global room_states
    room_id = 1

    # Finde einen nicht vollen Raum oder erstelle einen neuen
    while str(room_id) in room_states and room_states[str(room_id)] >= 2:
        room_id += 1

    room_key = str(room_id)
    if room_key in room_states:
        room_states[room_key] += 1
        is_room_full = True
    else:
        room_states[room_key] = 1
        is_room_full = False

    response = HttpResponseRedirect(f'/game_{room_key}')
    response.set_cookie('roomID', room_key, path=f'/game_{room_key}/')
    response.set_cookie('is_room_full', str(is_room_full), path=f'/game_{room_key}/')

    return response

@csrf_exempt
def request_lobby(request):
    global room_states
    JSON = json.dumps(room_states)
    print(JSON)

    return HttpResponse(JSON)

    

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
