from django.contrib import admin
from .models import Users
from django.contrib.auth import admin as admin_auth_django
from .forms import UserChangeForm,UserCreationForm

@admin.register(Users) #registrando a model criada
class UsersAdmin(admin_auth_django.UserAdmin): #herda da classe ja existente do django
    form = UserChangeForm
    add_form = UserCreationForm
    model = Users
    fieldsets = admin_auth_django.UserAdmin.fieldsets + ( ('Cargo', {'fields' : ('cargo',)}),) # pegua os campos que ja existem em admin + o campo criado
