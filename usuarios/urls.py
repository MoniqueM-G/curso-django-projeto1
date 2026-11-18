from django.urls import path
from . import views
urlpatterns = [
    path('cadastrar_chef/',views.cadastrar_chef, name="cadastrar_chef")
]