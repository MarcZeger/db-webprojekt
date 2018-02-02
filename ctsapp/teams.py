from .models import *

def get_team_members(team_id):
    liste = []
    for member_id in Spieler.objects.raw("SELECT * FROM spieler WHERE team_id_id = " + str(team_id) + " ORDER BY punktzahl DESC"):
        liste.append(member_id)
    return(liste)