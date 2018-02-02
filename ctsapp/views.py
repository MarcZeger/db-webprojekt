from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

import math
from .functions import *
from .models import *

from .teams import *

from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def index(request):
    best_spots = get_best_spots()
    best_spieler = get_best_spieler()
    liste = {'spielers':best_spieler, 'spots':best_spots}
    return(render(request,'ctsapp/index.html', liste))

def kontakt(request):
    return(render(request,'ctsapp/kontakt.html'))

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
                user = Spieler(username=username, first_name=first_name, last_name=last_name, ort_id=Ort(ort_id=1), email = email, punktzahl=0)
                user.set_password(password)
                user.save()
                message = {'message':"Sie haben sich erfolgreich registriert!"}


        #Eventuell direkter login von User?
        #login(request, user)
        return render(request,'ctsapp/registrierung.html',message)

    else:
        return render(request,"ctsapp/registrierung.html")


def teams(request):
    if (request.user.is_authenticated):
        if (request.user.team_id):
            mitglieder = get_team_members(request.user.team_id.team_id)
            members = {'members': mitglieder}
            return render(request, 'ctsapp/teams.html', members)
            print(members)
        else:
            return render(request,'ctsapp/team_erstellen.html')
    else:
        return redirect('index')

def spot_suche(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            code = request.POST['code']
            try:
                spot = Spot.objects.get(code=code)
            except:
                spot = None

            if spot != None:
                warda = check_spieler_spot(spot.spot_id,request.user.spieler_id)
                if  warda == False:
                    spot_punktzahl = spot.schwierigkeit_id.punkte
                    spieler = Spieler.objects.get(spieler_id = request.user.spieler_id)
                    spieler.punktzahl += spot_punktzahl
                    spieler.save()
                    set_spieler_spot(spot_id=spot,spieler_id=spieler)
                    meldung = {'message_code':'Eingabe des Codes war erfolgreich!','flag':'success','punktzahl':spot_punktzahl}
                else:
                    meldung = {'message_code':'Der Code wurde bereits von dir eingegeben!', 'datum':warda,'flag':'danger'}
            else:
                meldung = {'message_code': 'Der eingegebene Code ist leider falsch!','flag':'danger'}
            return (render(request, "ctsapp/spot_suche.html", meldung))

        else:
            spots = ""
            message = ""
            ort = ""
            try:
                ort = request.GET['ort']
            except:
                return(render(request,'ctsapp/spot_suche.html'))
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
    else:
        return(redirect('/login'))

def spot_detail(request, spot_id):
    if request.user.is_authenticated:
        spot = get_spot(spot_id)
        bilder = Medium.objects.filter(spot_id=spot_id)
        counter = 0
        for bild in bilder:
            if counter == 0:
                bild.first = "active"
                counter += 1
            else:
                bild.first = ""
        bewertungen = get_bewertungen(spot_id)
        liste = {'spot':spot, 'bilder':bilder, 'bewertungen':bewertungen}
        return render(request,'ctsapp/spot_detail.html', liste)
    else:
        return (redirect('/login'))