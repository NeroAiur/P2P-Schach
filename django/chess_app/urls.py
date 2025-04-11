from django.urls import path

from . import views 

urlpatterns = [
    path('', views.index, name="index"),
    # IDEE, nicht finaler Code
    path('/login', views.send_login_data_to_login_function, name="login"),
    # IDEE, nicht finaler Code
    path('/game', views.get_move_to_game_calc, name="game"),
    # IDEE, nicht finaler Code
    path('/game', views.send_move_to_game_calc, name="game"),
]