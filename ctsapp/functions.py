from .models import *
import math

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