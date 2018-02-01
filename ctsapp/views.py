from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    return(render(request,'ctsapp/index.html'))

def zahl(request, zahl):
    zahl = {'zahl':zahl}
    return(render(request,'ctsapp/index.html', zahl))

def login_custom(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return(redirect("index"))
            else:
                fehler = {'fehler':"Login-Daten nicht korrekt!"}
                return(render(request,'registration/login.html', fehler))
        else:
            return(render(request,'registration/login.html'))
