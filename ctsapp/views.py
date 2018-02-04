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
    all_spots = Spot.objects.all()
    center = get_map_center(all_spots)
    liste = {'spielers':best_spieler, 'best_spots':best_spots,'spots':all_spots,'center':center}
    return(render(request,'ctsapp/index.html', liste))

def kontakt(request):
    return(render(request,'ctsapp/kontakt.html'))

def zahl(request, zahl):
    zahl = {'zahl':zahl}
    return(render(request,'ctsapp/index.html', zahl))

def profil(request):
    punktzahl = request.user.punktzahl
    punktzahl = float(punktzahl)
    if (punktzahl == 0):
        level = 1
    else:
        level = math.floor( math.log10(punktzahl+20) / math.log10(1.25) - math.log10(20) / math.log10(1.25) ) +1
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
        if request.POST['seite'] == "1":
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            ort_plz = request.POST['plz']
            orte = get_ort_liste(ort_plz)
            werte = {'username':username,'first_name':first_name,'last_name':last_name,'orte':orte,'email':email,'plz':ort_plz}
            if Spieler.objects.filter(username=username).exists():
                message = {'message': "Benutzername bereits vergeben!", 'flag': 'wrong'}
                werte.update(message)
            else:
                if Spieler.objects.filter(email=email).exists():
                    message = {'message': "E-Mail Addresse bereits hinterlegt!", 'flag': 'wrong'}
                    werte.update(message)
            return(render(request,'ctsapp/registrierung_2.html',werte))

        elif request.POST['seite'] == "2":
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            ort_id = request.POST['ort']
            email = request.POST['email']
            werte = {'username': username, 'first_name': first_name, 'last_name': last_name, 'ort': ort_id,'email':email}
            return(render(request,'ctsapp/registrierung_3.html',werte))

        elif request.POST['seite'] == "3":
            print("schritt 3")
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            ort_id = request.POST['ort']
            email = request.POST['email']
            password = request.POST['password']
            werte = {}
            if Spieler.objects.filter(username=username).exists():
                print("Benutzername bereits vergeben")
                message = {'message': "Benutzername bereits vergeben!", 'flag': 'wrong'}
                werte.update(message)
            else:
                print("Benutzername nicht vergeben")
                if Spieler.objects.filter(email=email).exists():
                    print("Email vergeben!")
                    message = {'message': "E-Mail Addresse bereits hinterlegt!", 'flag': 'wrong'}
                    werte.update(message)
                else:
                    print("Benutzer wird angelegt")
                    user = Spieler(username=username, first_name=first_name, last_name=last_name, ort_id=Ort(ort_id=ort_id),
                                   email=email, punktzahl=0)
                    user.set_password(password)
                    user.save()
                    message = {'message': "Sie haben sich erfolgreich registriert!"}
                    # Eventuell direkter login von User?
                    # login(request, user)
                    return render(request, 'ctsapp/registrierung_1.html', message)
            return(render(request,'ctsapp/registrierung_1.html'))

        #Seite neuer Ort anzeigen und Werte uebergeben
        elif request.POST['seite'] == "4":
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            plz = request.POST['plz']
            werte = {'username': username, 'first_name': first_name, 'last_name': last_name, 'plz': plz,'email': email}
            return(render(request,'ctsapp/registrierung_neuer_ort.html',werte))

        #Neuer Ort Formular erhalten, neuen Ort anlegen und weiterleiten
        elif request.POST['seite'] == "5":
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            ort_plz = request.POST['ort_plz']
            ort_name = request.POST['ort_name']
            ort_id = new_ort(ort_plz,ort_name)
            werte = {'username': username, 'first_name': first_name, 'last_name': last_name, 'ort': ort_id, 'email': email}
            return (render(request, 'ctsapp/registrierung_3.html', werte))

    else:
        return render(request, "ctsapp/registrierung_1.html")



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
        #Code wurde eingegeben - Keine Suche
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
                spots = get_spot_list(ort)
                if type(spots) == str:
                    message = spots
                else:
                    spots = add_img_url(spots)

            else:
                spots = add_img_url(Spot.objects.all())
            spot_list = []
            if spots != None and spots != [] and type(spots) != str:
                for spot in spots:
                    spot.bewertung = range(int(spot.bewertung))
                    spot_list.append(spot)
                print(spot_list)
            else:
                message = spots
            liste = {'spots':spot_list,'message':message}
            return render(request,'ctsapp/spot_suche.html',liste)
    else:
        return(redirect('/login'))

def spot_detail(request, spot_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            spot = get_spot(spot_id)
            bilder = get_bilder(spot_id)
            bewertungen = get_bewertungen(spot_id)
            liste = {'spot':spot, 'bilder':bilder, 'bewertungen':bewertungen}

        else:
            #Bild speichern
            spot_id = request.POST['spot']
            file = request.FILES['file']
            type = "bild"
            path = save_file(file,spot_id,request.user.spieler_id)
            create_medium(path,request.user.spieler_id,spot_id,type)
            #Webseite zurückgeben
            spot = get_spot(spot_id)
            bilder = get_bilder(spot_id)
            bewertungen = get_bewertungen(spot_id)
            liste = {'spot': spot, 'bilder': bilder, 'bewertungen': bewertungen,'meldung':"Bild wurde erfolgreich hochgeladen!"}
        return render(request, 'ctsapp/spot_detail.html', liste)
    else:
        return (redirect('/login'))

def impressum(request):
    return(render(request,'ctsapp/impressum.html'))