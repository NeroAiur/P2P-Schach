from django.urls import path

from .views import * 

urlpatterns = [
    path('', index, name="index"),
    # IDEE, nicht finaler Code

    path('game',         GameView.as_view(),       name="game"),
    path('scoreboard',   ScoreboardView.as_view(), name='scoreboard'),
    # path('profile/<ID>', ProfileView.as_view(),    name="profile"),

    # path('login',                              send_login_data_to_login_function, name="login"),
    # path('game/<room_<room_ID>/send_gamestate', send_gamestate,                    name="send_gamestate"),
    # path('profile/<ID>/update_<elo>',          change_profile_name(),             name="change_elo"),

]