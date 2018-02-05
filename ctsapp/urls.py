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
    path('teams/', views.teams, name='teams'),
    path('team_erstellen/', views.team_erstellen, name='team_erstellen'),
    path('suche/', views.spot_suche, name="suche"),
    path('spot/<int:spot_id>', views.spot_detail, name='spot_detail'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('impressum/', views.impressum, name="impressum"),
    path('administration/', views.administration, name="administration"),
    path('api/get-ort/<int:plz>', views.ort_api, name='ort_api'),
    path('api/get-code/', views.code_api, name='code_api')
]
