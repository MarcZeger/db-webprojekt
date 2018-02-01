from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .functions import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist

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

def registrierung(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        ort_plz = request.POST['plz']
        ort = request.POST['ort']
        email = request.POST['email']

        if Spieler.objects.filter(username=username).exists():
            message = {'message': "Benutzername bereits vergeben!",'flag':'wrong'}
        else:
            if Spieler.objects.filter(email=email).exists():
                message = {'message': "E-Mail Addresse bereits hinterlegt!",'flag':'wrong'}
            else:
                user = Spieler(username=username, first_name=first_name, last_name=last_name, ort_id=Ort(ort_id=1), email = email)
                user.set_password(password)
                user.save()
                message = {'message':"Sie haben sich erfolgreich registriert!"}


        #Eventuell direkter login von User?
        #login(request, user)
        return(render(request,'ctsapp/registrierung.html',message))

    else:
        return(render(request,"ctsapp/registrierung.html"))

def spot_suche(request):
    ort = request.GET['ort']
    spots = ""
    message = ""
    if ort != "":
        ort_id = get_ort_id(ort)
        if type(ort_id) == int:
            spots = Spot.objects.filter(ort_id=ort_id)
        else:
            message = ort_id
            print(message)
    else:
        spots = Spot.objects.all()
    spot_list = []
    if spots != None and spots != []:
        for spot in spots:
            spot.bewertung = range(int(spot.bewertung))
            spot_list.append(spot)
        print(spot_list)
    liste = {'spots':spot_list,'message':message}
    return render(request,'ctsapp/spot_suche.html',liste)

def spot_detail(request, spot_id):
    spots = Spot.objects.get(spot_id=spot_id)
    bilder = Medium.objects.filter(spot_id=spot_id)
    print(bilder)
    liste = {'spot':spots, 'bilder':bilder}
    return render(request,'ctsapp/spot_detail.html', liste)