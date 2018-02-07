from django.urls import path, include
from django.conf.urls import url, handler400, handler403, handler404, handler500
from django.contrib.auth import views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url('^', include('django.contrib.auth.urls')),
    path('login-fehler/', views.login_custom, name='login_custom'),
    #path('logout/', views.logout, name="logout"),
    #path('register/', views.register)
    path('profil/', views.profil, name='profil'),
    path('registrierung/', views.registrierung, name='registrierung'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('mein_team/', views.mein_team, name='mein_team'),
    path('team_erstellen/', views.team_erstellen, name='team_erstellen'),
    path('suche/', views.spot_suche, name="suche"),
    path('spot/<int:spot_id>', views.spot_detail, name='spot_detail'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('impressum/', views.impressum, name="impressum"),
    path('administration/', views.administration, name="administration"),
    path('api/get-ort/<str:plz>', views.ort_api, name='ort_api'),
    path('api/get-code/', views.code_api, name='code_api'),
    path('api/get-spot/',views.spot_api, name='spot_api'),
    path('api/get-user/',views.user_api, name='user_api'),
    path('api/get-team/',views.team_api, name='team_api'),
    path('spot-loeschen/',views.spot_loeschen, name='spot_loeschen'),
    path('user-sperren/', views.user_sperren, name='user_sperren'),
    path('user-loeschen/', views.user_loeschen, name='user_loeschen'),
    path('team-loeschen/', views.team_loeschen, name='team_loeschen'),
    path('user-team-entfernen/', views.user_team_entfernen, name='user_team_entfernen'),
    path('bewertung/<int:spot_id>', views.make_bewertung, name='make_bewertung'),
    path('user-team-add/', views.user_team_add, name='user_team_add'),
    path('team_verlassen/', views.team_verlassen, name='team_verlassen'),
    path('teams/', views.teams, name='teams')

]
