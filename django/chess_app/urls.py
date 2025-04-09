from django.urls import path

from . import views 

urlpatterns = [
    path('', views.index, name="index"),
    # IDEE, nicht finaler Code
    path('/login', views.send_login_data_to_login_function, name="login"),
]