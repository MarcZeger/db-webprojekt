from .models import *

def get_team_members(team_id):
    for member_id in Spieler.objects.raw("SELECT spieler_id FROM spieler WHERE team_id_id =" + str(team_id)):
        print(member_id)