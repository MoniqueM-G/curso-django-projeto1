from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# HTTP REQUEST
def home(request):
    return HttpResponse("home")
#HTTP RESPONSE

def contato(request):
    return HttpResponse("contato")


def sobre(request):
    return HttpResponse("sobre")
