from django.urls import path, include
from django.conf.urls import url, handler400, handler403, handler404, handler500
from django.contrib.auth import views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url('^', include('django.contrib.auth.urls')),
    path('login-fehler/', views.login_custom, name='login_custom'),
    #path('logout/', views.logout, name="logout"),
    path('registrierung/', views.registrierung, name='registrierung'),
    path('suche/', views.spot_suche, name="suche"),
    path('spot/<int:spot_id>', views.spot_detail, name='spot_detail')
]
