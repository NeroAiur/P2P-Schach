import io
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
from backend.Game import *

def index(request):
    return render(request, "index.html")



# PSEUDOCODE/IDEE
@csrf_exempt
def register_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    add_user("../db/user.db", username, password)
    uID = get_uID("../db/user.db", username, password)

    response = HttpResponseRedirect('dashboard')
    response.set_cookie('userID', uID, path='dashboard')

    return response



@csrf_exempt
def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user_login("../db/user.db", username, password)
    uID = get_uID("../db/user.db", username, password)

    response = HttpResponseRedirect('dashboard')
    response.set_cookie('userID', uID, path='dashboard')

    return response



@csrf_exempt
def render_dashboard(request):

    return render(request, "dashboard.html")

@csrf_exempt
def render_game(request, roomID):
    context = {
        'roomID' : roomID,
    }
    return render(request, "chessboard.html", context)



rooms = []
room_id = 1

@csrf_exempt
def create_game_room(request):
    global rooms
    global room_id
    room  = {}

    uID = request.POST.get('userID')

    room.update({"room_id": room_id, "white": uID, "black": "none", "turn": 1})

    rooms.append(room)

    response = HttpResponseRedirect(f'/game_{room_id}')
    response.set_cookie('room_id', room_id, path=f'/game_{room_id}')
    response.set_cookie('side', 'white', path=f'/game_{room_id}')

    return response



@csrf_exempt
def join_lobby(request):
    global rooms

    room_id = request.POST.get('roomID')
    uID = request.POST.get('userID')


    for room in rooms:
        if int(room['room_id']) == int(room_id):
            joined_room = room

    joined_room['black'] = uID
    # players
    player1 = Player(joined_room['white'], "white")
    player2 = Player(joined_room['black'], "black")

    g = Game(player1, player2)

    joined_room.update({'game' : g})

    response = HttpResponseRedirect(f'/game_{room_id}')
    response.set_cookie('room_id', room_id, path=f'/game_{room_id}')
    response.set_cookie('side', 'black', path=f'/game_{room_id}')

    print(joined_room)

    return response



@csrf_exempt
def send_move(request):
    global rooms
    request_body = json.loads(request.body.decode('utf-8'))
    roomID = request_body['roomID']
    move = request_body['move']

    for room in rooms:
        if int(room['room_id']) == int(roomID):
            joined_room = room
    
    new_state = joined_room['game'].run_turn(move)

    joined_room['turn'] = joined_room['turn'] + 1

    JSON = {
        "game": new_state,
        "turn": joined_room['turn']
    }

    return HttpResponse(json.dumps(JSON))



@csrf_exempt
def request_gamestate(request):
    global rooms
    request_body = json.loads(request.body.decode('utf-8'))
    roomID = request_body['roomID']

    for room in rooms:
        if int(room['room_id']) == int(roomID):
            joined_room = room
    new_state = joined_room['game'].return_gamestate()

    
    JSON = {
        "game": new_state,
        "turn": joined_room['turn']
    }


    return HttpResponse(json.dumps(JSON))

@csrf_exempt
def await_game(request):
    global rooms
    request_body = json.loads(request.body.decode('utf-8'))
    roomID = request_body['roomID']

    for room in rooms:
        if int(room['room_id']) == int(roomID):
            joined_room = room
    response = {"black": joined_room['black']} 

    return HttpResponse(json.dumps(response))

@csrf_exempt
def request_lobby(request):
    global rooms

    JSON = json.dumps(rooms)
    return HttpResponse(JSON)

    

class DashboardView(TemplateView):
    template_name = "dashboard.html"


# class ProfileView(TemplateView):
#     template_name = "home.html"
#     add_user(dbpath, username, password)
#     return render(request, "base.html")

