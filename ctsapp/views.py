from django.shortcuts import render, HttpResponse
from django.http import HttpResponse

# Create your views here.
def index(request):
    return(HttpResponse("Hallo"))

def zahl(request, zahl):
    zahl = {'zahl':zahl}
    return(render(request,'ctsapp/index.html', zahl))
#return(HttpResponse(zahl))
