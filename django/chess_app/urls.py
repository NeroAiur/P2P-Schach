from django.urls import path

from .views import * 

urlpatterns = [
    path('',                index,              name="index"),
    path('create_game',     create_game_room,   name="create_game"),
    path('game_<roomID>',   render_game,        name='game'),
    path('dashboard',       render_dashboard,   name='dashboard'),
    path('register',        register_user,      name="register"),
    path('login',           login_user,         name="login"),
    path('join',            join_lobby,         name="join"),
    path('lobby',           request_lobby,      name="lobby"),
    path('send_move',       send_move,          name="send_move"),
    path('await_game',       await_game,          name="await_game")
    # path('game/<room_<room_ID>/send_gamestate', send_gamestate,                    name="send_gamestate"),
    # path('profile/<ID>/update_<elo>',          change_profile_name(),             name="change_elo"),

    # path('/login', send_login_data_to_login_function, name="login"),
    # IDEE, nicht finaler Code
    # path('/game', get_move_to_game_calc, name="game"),
    # IDEE, nicht finaler Code
    # path('/game', send_move_to_game_calc, name="game"),
]