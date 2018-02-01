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
]
