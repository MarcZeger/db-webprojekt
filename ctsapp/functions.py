from .models import *
import math
import time
from django.core.files.storage import default_storage
from random import randint
from operator import itemgetter
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
import os
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
import geopy
from django.forms.models import model_to_dict

def get_bild_link(spot_id):
    bilder = Medium.objects.filter(spot_id=spot_id)
    for bild in bilder:
        return(bild.link)

def get_ort_id(ortname):
    try:
        ort = Ort.objects.get(name=ortname)
    except Ort.DoesNotExist:
        ort = "Leider konnten keine Ergebnisse gefunden werden!"
    if ort == "Leider konnten keine Ergebnisse gefunden werden!":
        return(ort)
    else:
        return(ort.ort_id)

def get_team_members(team_id):
    liste = []
    for member_id in Spieler.objects.raw("SELECT * FROM spieler WHERE team_id_id = " + str(team_id) + " ORDER BY punktzahl DESC"):
        liste.append(member_id)
    return(liste)

def get_teamid_by_name(teamname):
    liste=[]
    for o in Team.objects.filter(name__icontains = teamname):
        liste.append(o.team_id)
    return (liste)

def set_teamid_to_user(name, user):
    spieler = Spieler.objects.get(username=user)
    t_id = get_teamid_by_name(name)
    spieler.team_id_id = int(t_id[0])
    spieler.save()

def add_user_to_team(spieler_id,team_id):
    spieler = Spieler.objects.get(spieler_id=spieler_id)
    spieler.team_id = team_id
    spieler.save()

def create_new_team(name):
    team = Team(name=name)
    team.save()

def get_team_punkte(mitglieder):
    punkte = 0
    for member in mitglieder:
        punkte_int = int(member.punktzahl)
        punkte += punkte_int
    return(punkte)

def get_bewertungen(spot_id):
    bewertungen = SpielerBewertetSpot.objects.filter(spot_id=spot_id)
    for bewertung in bewertungen:
        bewertung.bewertung = range(int(bewertung.bewertung))
    return(bewertungen)

def get_spot(spot_id):
    spot = Spot.objects.get(spot_id=spot_id)
    spot.bewertung = range(spot.bewertung)
    return spot

def get_best_spots():
    spots = Spot.objects.all().order_by('-bewertung')
    liste = []
    counter = 1
    for spot in spots:
        if counter < 4:
            spot.bewertung = range(spot.bewertung)
            spot.bild = get_bild_link(spot.spot_id)
            liste.append(spot)
            counter += 1
        else:
            return(liste)

def get_best_spieler():
    spielers = Spieler.objects.all().order_by('-punktzahl')
    liste = []
    counter = 1
    for spieler in spielers:
        spieler.profilbild_url = get_profilbild_url(spieler.spieler_id)
        if counter == 1:
            spieler.active = "active"
            liste.append(spieler)
            counter += 1
        elif counter < 4:
            liste.append(spieler)
            spieler.active = ""
            counter += 1
        else:
            return(liste)

def get_best_team():
    teams = Team.objects.all()
    liste2 = []
    counter = 1
    for team in teams:
        team.punkte = get_teampunkte(team.team_id)
    new_team = sort_team(teams)
    for team in new_team:
        if counter == 1:
            team.is_active = "active"
            liste2.append(team)
            counter += 1
        elif counter < 4:
            team.is_active = ""
            liste2.append(team)
            counter += 1
    return(liste2)

def sort_team(teams):
    p1 = 0
    p2 = 0
    p3 = 0
    list_team = [p1, p2, p3]
    for team in teams:
        par = int(team.punkte)
        if par > p1:
            p3 = p2
            p2 = p1
            p1 = par
            list_team[2] = list_team[1]
            list_team[1] = list_team[0]
            list_team[0] = team
        elif par <= p1 and par > p2:
            p3 = p2
            p2 = par
            list_team[2] = list_team[1]
            list_team[1] = team
        elif par >= p3 and par <= p2:
            p3 = par
            list_team[2] = team
    return list_team

def get_teampunkte(team_id):
    liste = []
    for member_id in Spieler.objects.raw(
            "SELECT * FROM spieler WHERE team_id_id = " + str(team_id) + " ORDER BY punktzahl DESC"):
        liste.append(member_id)
    punkte = 0
    for member in liste:
        punkte_int = int(member.punktzahl)
        punkte += punkte_int
    return (punkte)
 
def get_level(punktzahl):
    punktzahl = float(punktzahl)
    if (punktzahl < 1):
        level = 1
        UG = 0
        OG = 5
        levelUG = 0
        levelOG = 5
        ProUG = 0
        ProOG = 100
    else:
        level = math.floor(math.log10(punktzahl + 20) / math.log10(1.25) - math.log10(20) / math.log10(1.25)) + 1
        levelUG = 20 * 1.25 ** (level - 1) - 20
        UG = math.ceil(punktzahl - levelUG)
        levelOG = 20 * 1.25 ** (level) - 20
        OG = math.ceil(levelOG - punktzahl)
        ges = OG + UG
        ProUG = UG / ges * 100
        ProOG = OG / ges * 100
    liste = {'level': level, 'UG': UG, 'OG': OG, 'levelUG': levelUG, 'levelOG': levelOG, 'ProOG': ProOG, 'ProUG': ProUG}
    return liste
  
def check_spieler_spot(spot_id, spieler_id):
    try:
        check = SpielerEntdecktSpot.objects.get(spot_id=spot_id,spieler_id=spieler_id)
    except:
        check = None
    if check == None:
        return(False)
    else:
        return(check.datum)

def set_spieler_spot(spot_id, spieler_id):
    wert = SpielerEntdecktSpot.objects.create(spieler_id=spieler_id,spot_id=spot_id, datum=get_time())
    wert.save()

def get_time():
    return(time.strftime("%Y-%m-%d %H:%M:%S"))

def get_ort_liste(plz):
    orte = Ort.objects.filter(plz=plz)
    return(orte)

def new_ort(plz,name):
    ort = Ort.objects.create(name=name,plz=plz)
    ort.save()
    return(ort.ort_id)

def get_spot_list(ortname):
    orte = Ort.objects.filter(name__icontains=ortname)
    spots = []
    for ort in orte:
        ort_spots = Spot.objects.filter(ort_id=ort.ort_id)
        for spot in ort_spots:
            spots.append(spot)
    if spots == []:
        return("Leider konnten keine Ergebnisse gefunden werden!")
    return(spots)

def get_team_list(teamname):
    team = Team.objects.filter(name__icontains=teamname)
    return(team)

def save_file(file,spot_id,user_id):
    path = str(time.strftime("%Y-%m-%d-%H%M%S"))+str(user_id)+"_Spot_"+str(spot_id)+"_"+str(file.name)
    with default_storage.open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return("/media/"+str(path))

def save_profilbild(file,user_id):
    user = Spieler.objects.get(spieler_id=user_id)
    if has_profilbild(user):
        delete_profilbild(user)
    path = str(time.strftime("%Y-%m-%d-%H%M%S"))+str(user_id)+"_profilbild_"+str(file.name)
    with default_storage.open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return("/media/"+str(path))

def create_medium(path,user_id,spot_id,dateityp):
    spieler = Spieler.objects.get(spieler_id = user_id)
    spot = Spot.objects.get(spot_id=spot_id)
    datum = get_time()
    medium = Medium.objects.create(dateityp=dateityp,link=path,spieler_id=spieler,spot_id=spot,erstelldatum=datum,profilbild_flag=0)
    medium.save()

def create_profilbild(path,user_id,dateityp):
    spieler = Spieler.objects.get(spieler_id = user_id)
    datum = get_time()
    medium = Medium.objects.create(dateityp=dateityp,link=path,spieler_id=spieler,erstelldatum=datum,profilbild_flag=1)
    medium.save()

def get_medium(spot_id):
    medien = Medium.objects.filter(spot_id=spot_id)
    counter = 0
    for medium in medien:
        if counter == 0:
            medium.first = "active"
            counter += 1
        else:
            medium.first = ""
    return(medien)

def get_map_center(spots):
    min_lat = float
    max_lat = float
    min_lon = float
    max_lon = float
    count = 1
    for spot in spots:
        koordinate_b = float(spot.breitengrad)
        koordinate_l = float(spot.laengengrad)
        if count == 1:
            min_lat = koordinate_b
            max_lat = koordinate_b
            min_lon = koordinate_l
            max_lon = koordinate_l
            count = 2
        else:
            if (koordinate_b <= min_lat):
                min_lat = koordinate_b
            if (koordinate_b >= max_lat):
                max_lat = koordinate_b
            if (koordinate_l <= min_lon):
                min_lon = koordinate_l
            if (koordinate_l >= max_lon):
                max_lon = koordinate_l
    lon = min_lon + ((max_lon-min_lon)/2)
    lat = min_lat + ((max_lat - min_lat)/2)
    return(str(lat)+","+str(lon))

def add_img_url(spot_list):
    for spot in spot_list:
        bild = Medium.objects.filter(spot_id=spot.spot_id)
        try:
            spot.bild_url = bild[0].link
        except:
            spot.bild_url = "https://upload.wikimedia.org/wikipedia/commons/3/39/Simpleicons_Places_map-with-placeholder.svg"

    return(spot_list)
  

def create_spot_code():
    buchstabe_k = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    buchstabe_g = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                   'U', 'V', 'W', 'X', 'Y', 'Z']
    code = ""
    for i in range(6):
        choice = randint(0,2)
        if choice == 0:
            code += buchstabe_k[randint(0,23)]
        elif choice == 1:
            code += buchstabe_g[randint(0,23)]
        else:
            code += str(randint(0,9))
    #In Datenbank prüfen, ob code bereits verwendet wird
    if Spot.objects.filter(code = code).exists():
        create_spot_code()
    else:
        return(code)

def get_spielers(username):
    spielers = Spieler.objects.filter(username__icontains=username)
    return(spielers)

def get_teamname_by_id(team_id):
    team = Team.objects.get(team_id=team_id)
    return team.name

def get_besuchte_spots(user_id):
    user = Spieler.objects.get(spieler_id = user_id)
    visited = SpielerEntdecktSpot.objects.filter(spieler_id = user)
    spots = []
    for visit in visited:
        spot = Spot.objects.get(spot_id=visit.spot_id.spot_id)
        spots.append(spot)
    return(spots)

def update_bewertung(spot_id):
    spot = Spot.objects.get(spot_id=spot_id)
    bewertungen = SpielerBewertetSpot.objects.filter(spot_id=spot)
    summe = 0
    for bewertung in bewertungen:
        summe += bewertung.bewertung
    bewertung_neu = round((summe/len(bewertungen)))
    spot.bewertung = bewertung_neu
    spot.save()

def get_profilbild_url(user_id):
    try:
        medium = Medium.objects.get(spieler_id=user_id, profilbild_flag=1)
        return(medium.link)
    except:
        return("/static/Bilder/goat.png")

def send_actication_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Aktivierung des CTS Account'
    message = render_to_string('email/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf8'),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.content_subtype = "html"
    email.send()

def check_file(filepath):
    extension = os.path.splitext(filepath)
    bilder = ['.jpg','.tif','.png','.gif','.psd', '.jpeg']
    videos = ['.mpg','.mpeg','.mp4']
    if extension[1].lower() in bilder:
        return('bild')
    elif extension[1].lower() in videos:
        return('video')
    else:
        return False

def mail_gesperrt(spieler):
    mail_subject = 'Sperrung des Accounts'
    message = render_to_string('email/spieler_gesperrt.html', {

    })
    to_email = spieler.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.content_subtype = "html"
    email.send()

def get_distance(spot, ort):
    # ort = geopy.geocoders.GoogleV3('AIzaSyBt2fnvdE4Za0wT6b129B4yxN48SbxFXYE').geocode(ort.name, True)
    koordinate1 = ort
    koordinate2 = (spot.breitengrad, spot.laengengrad)
    return(vincenty(koordinate1, koordinate2).kilometers)

def get_koordinate(ort):
    geolocator = Nominatim()
    location = geolocator.geocode(str(ort.name))
    result = (location.latitude, location.longitude)
    return(result)

def get_spots_umkreis(ort, umkreis):
    spots = Spot.objects.all()
    output = []
    for spot in spots:
        if get_distance(spot,ort) <= umkreis:
            cache = model_to_dict(spot)
            cache['schwierigkeit'] = spot.schwierigkeit_id.beschreibung
            cache['ortname'] = spot.ort_id.name
            cache['bildurl'] = get_bild_link(spot.spot_id)
            del cache['code']
            output.append(cache)
    if output == []:
        return False
    else:
        return(output)

def delete_team(team):
    users = Spieler.objects.filter(team_id=team.team_id)
    for user in users:
        user.team_id = None
        user.save()
    team.delete()

def has_profilbild(user):
    try:
        medium = Medium.objects.filter(spieler_id=user.spieler_id, profilbild_flag=True)
        return True
    except:
        return False

def delete_profilbild(user):
    medium = Medium.objects.filter(spieler_id=user.spieler_id, profilbild_flag=True)
    medium.delete()
