from django.shortcuts import render
from backend.database_ops import add_user

def index(request):
    return render(request, "base.html")

# PSEUDOCODE/IDEE
def send_login_data_to_login_function(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    # nicht ganz sicher, was dbpath ist
    add_user(dbpath, username, password)
    return render(request, "base.html")