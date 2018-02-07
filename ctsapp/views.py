from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth import authenticate, login, logout

import math
from .functions import *
from .models import *

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
    if request.user.is_authenticated:
        liste = get_level(request.user.punktzahl)
        return (render(request, 'ctsapp/profil.html', liste))
    else:
        return (redirect('login'))

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

def mein_team(request):
    if (request.user.is_authenticated):
        if (request.user.team_id):
            mitglieder = get_team_members(request.user.team_id.team_id)
            punkte = get_team_punkte(mitglieder)
            werte = {'members' : mitglieder, 'punkte' : punkte}
            return render(request, 'ctsapp/mein_team.html', werte)
        else:
            return redirect('team_erstellen')
    else:
        return redirect('index')

def team_erstellen(request):
    if (request.user.is_authenticated):
        if (request.user.team_id):
            return redirect('teams')
        else:
            if request.method == "POST":
                name = request.POST['name']
                if Team.objects.filter(name=name).exists():
                    message = {'message': "Teamname bereits vergeben!", 'flag': 'wrong'}
                else:
                    create_new_team(name)
                    set_teamid_to_user(name, request.user.username)
                    message = {'message': "Sie haben erfolgreich das Team " + str(name) + " erstellt"}
                return render(request, 'ctsapp/team_erstellen.html', message)
            else:
                return render(request, "ctsapp/team_erstellen.html")
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

def administration(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            bezeichnung = request.POST['bezeichnung']
            beschreibung = request.POST['beschreibung']
            laengengrad = request.POST['laengengrad']
            breitengrad = request.POST['breitengrad']
            plz = request.POST['plz']
            ort_id = request.POST['ort_id']
            schwierigkeit = request.POST['schwierigkeit']
            code = request.POST['code']
            ort = Ort.objects.get(ort_id=ort_id)
            schwierigkeit = Schwierigkeit.objects.get(schwierigkeit_id=schwierigkeit)
            spot = Spot.objects.create(code=code,bezeichnung=bezeichnung,beschreibung=beschreibung,bewertung=0,ort_id=ort,schwierigkeit_id=schwierigkeit,laengengrad=laengengrad,breitengrad=breitengrad)
            meldung = {'meldung':True}
            return(render(request,'ctsapp/administration.html',meldung))

        else:
            schwierigkeiten = Schwierigkeit.objects.all()
            schwierigkeiten = {'schwierigkeiten':schwierigkeiten}
            return(render(request,'ctsapp/administration.html',schwierigkeiten))
    else:
        return (redirect('/login'))
    
def ort_api(request, plz):
    orte = get_ort_liste(plz)
    print(orte)
    result_list = list(orte.values('name', 'ort_id'))
    return(JsonResponse(result_list, safe = False))

def code_api(request):
    code = create_spot_code()
    return (JsonResponse({'code':code}, safe=False))

def spot_api(request):
    ortname = request.GET['ort']
    bezeichnung = request.GET['bezeichnung']
    spots_vor_bezeichnung = get_spot_list(ortname)
    if type(spots_vor_bezeichnung) == str:
        return JsonResponse({'spots':"Keine Ergebnisse"})
    if bezeichnung != "":
        spots_nach_bezeichnung = []
        for spot in spots_vor_bezeichnung:
            if spot.bezeichnung == bezeichnung:
                spots_nach_bezeichnung.append(spot)
    else:
        spots_nach_bezeichnung = spots_vor_bezeichnung
    spot_list = []
    dict = {}
    for item in spots_nach_bezeichnung:
        dict['spot_id'] = item.spot_id
        dict['bezeichnung'] = item.bezeichnung
        dict['ortname'] = item.ort_id.name
        dict['schwierigkeit'] = item.schwierigkeit_id.beschreibung
        spot_list.append(dict)
        dict = {}
    return(JsonResponse(spot_list, safe=False))

def spot_loeschen(request):
    spot_id = request.POST['spotid']
    spot = Spot.objects.get(spot_id=spot_id)
    spot.delete()
    return(render(request,'ctsapp/spot_geloescht.html'))

def user_api(request):
    username = request.GET['username']
    users = get_spielers(username)
    users = list(users.values('email','username','first_name','last_name','spieler_id','is_active','team_id'))
    return(JsonResponse(users, safe=False))

def team_api(request):
    teamname = request.GET['teamname']
    teamid = get_teamid_by_name(teamname)
    teams = []
    for id in teamid:
        teams.append(Team.objects.get(team_id=id))
    dict={}
    team_list = []
    for team in teams:
        dict['name'] = team.name
        dict['team_id'] = team.team_id
        team_list.append(dict)
        dict = {}
    return(JsonResponse(team_list,safe=False))

def user_sperren(request):
    spieler_id = request.POST['spieler_id']
    spieler = Spieler.objects.get(spieler_id=spieler_id)
    if spieler.is_active == 0:
        spieler.is_active = 1
    else:
        spieler.is_active = 0
    spieler.save()
    return(render(request,'ctsapp/spot_geloescht.html'))

def user_team_add(request):
    if (request.user.is_authenticated):
        spieler_id = request.POST['spieler_id']
        add_user_to_team(spieler_id, request.user.team_id)
        return redirect('mein_team')
    else:
        return redirect('index')

def user_loeschen(request):
    spieler_id = request.POST['spieler_id']
    spieler = Spieler.objects.get(spieler_id=spieler_id)
    spieler.delete()
    return (render(request, 'ctsapp/spot_geloescht.html'))

def team_loeschen(request):
    team_id = request.POST['team_id']
    team = Team.objects.get(team_id=team_id)
    team.delete()
    return (render(request, 'ctsapp/spot_geloescht.html'))

def teams(request):
    return (render(request, 'ctsapp/teams.html'))

def user_team_entfernen(request):
    spieler_id = request.POST['spieler_id']
    spieler = Spieler.objects.get(spieler_id=spieler_id)
    spieler.team_id = None;
    spieler.save()
    return (render(request, 'ctsapp/spot_geloescht.html'))

def team_verlassen(request):
    if (request.user.is_authenticated):
        if request.method == "POST":
            spieler = Spieler.objects.get(spieler_id=request.user.spieler_id)
            spieler.team_id = None;
            spieler.save()
            return render(request, 'ctsapp/team_wurde_verlassen.html')
    else:
        return redirect('ctsapp/index.html')

def make_bewertung(request, spot_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            spot = Spot.objects.get(spot_id=spot_id)
            user = Spieler.objects.get(spieler_id=request.user.spieler_id)
            bewertung_zahl = request.POST['bewertung_zahl']
            bewertung_text = request.POST['bewertung_text']
            bewertung = SpielerBewertetSpot.objects.create(bewertung = bewertung_zahl,bewertung_text=bewertung_text,spieler_id = user,spot_id=spot,datum=get_time())
            bewertung.save()
            return(redirect('/profil/'))
        else:
            spot = {'spot_id':spot_id}
            return(render(request,'ctsapp/bewertung.html',spot))
    else:
        return (redirect('/login'))

