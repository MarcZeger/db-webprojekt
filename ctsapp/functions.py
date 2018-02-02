from .models import *
import time

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