from .models import *
import time
from django.core.files.storage import default_storage

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

def get_bewertungen(spot_id):
    bewertungen = SpielerBewertetSpot.objects.filter(spot_id=spot_id)
    for bewertung in bewertungen:
        bewertung.bewertung = range(int(bewertung.bewertung))
        print(bewertung.datum)
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

def check_spieler_spot(spot_id, spieler_id):
    try:
        check = SpielerEntdecktSpot.objects.get(spot_id=spot_id,spieler_id=spieler_id)
    except:
        check = None
    if check == None:
        print("False")
        return(False)
    else:
        print(check.datum)
        return(check.datum)

def set_spieler_spot(spot_id, spieler_id):
    print("Set spieler spot")
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

def save_file(file,spot_id,user_id):
    path = str(time.strftime("%Y-%m-%d-%H%M%S"))+str(user_id)+"_Spot_"+str(spot_id)+"_"+str(file.name)
    with default_storage.open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return("/media/"+str(path))

def create_medium(path,user_id,spot_id,dateityp,profilbild=None):
    spieler = Spieler.objects.get(spieler_id = user_id)
    spot = Spot.objects.get(spot_id=spot_id)
    datum = get_time()
    if profilbild == None:
        profilbild = 0
    else:
        profilbild = 1
    medium = Medium.objects.create(dateityp=dateityp,link=path,spieler_id=spieler,spot_id=spot,erstelldatum=datum,profilbild_flag=profilbild)
    medium.save()

def get_bilder(spot_id):
    bilder = Medium.objects.filter(spot_id=spot_id)
    counter = 0
    for bild in bilder:
        if counter == 0:
            bild.first = "active"
            counter += 1
        else:
            bild.first = ""
    return(bilder)

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
        print(bild)
        try:
            spot.bild_url = bild[0].link
        except:
            spot.bild_url = "https://upload.wikimedia.org/wikipedia/commons/3/39/Simpleicons_Places_map-with-placeholder.svg"

    return(spot_list)