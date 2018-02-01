from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
import math
from .models import *

# Create your views here.
def index(request):
    return(render(request,'ctsapp/index.html'))

def zahl(request, zahl):
    zahl = {'zahl':zahl}
    return(render(request,'ctsapp/index.html', zahl))

def profil(request):
    punktzahl = request.user.punktzahl
    punktzahl = float(punktzahl)
    level = math.floor( math.log10(punktzahl) / math.log10(1.25) - math.log10(20) / math.log10(1.25) )
    levelUG = 20 * 1.25 ** level
    OG = math.ceil(punktzahl - levelUG)
    levelOG = 20 * 1.25 ** (level+1)
    UG = math.ceil(levelOG - punktzahl)
    ges = OG + UG
    ProUG = UG/ges *100
    ProOG = OG/ges *100
    liste = {'level': level, 'UG': UG, 'OG': OG, 'levelUG':levelUG, 'levelOG':levelOG, 'ProOG':ProOG, 'ProUG':ProUG}
    print(OG)
    print(UG)
    print(ges)
    print(ProUG)
    print(ProOG)
    print(ProOG+ProUG)
    return(render(request,'ctsapp/profil.html',liste))

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
