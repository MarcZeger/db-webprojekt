from .models import *
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
    for o in Team.objects.raw("SELECT * FROM team WHERE name = " + "'" + teamname + "'"):
        liste.append(o.team_id)
    return (liste)

def set_teamid_to_user(name, user):
    spieler = Spieler.objects.get(username=user)
    t_id = get_teamid_by_name(name)
    spieler.team_id_id = int(t_id[0])
    spieler.save()

def create_new_team(name):
    team = Team(name=name)
    team.save()

