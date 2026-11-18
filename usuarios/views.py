from django.http import HttpResponse
from django.shortcuts import render
from rolepermissions.decorators import has_permission_decorator

@has_permission_decorator('cadastrar_chef')
def cadastrar_chef(request):
    return HttpResponse('Teste')


# Create your views here.
