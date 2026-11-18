from rolepermissions.roles import AbstractUserRole

class Chef(AbstractUserRole):
    avaible_permissions = {
        'cadastrar_receita' : True,
        'cadastrar_chef' : True,
    }

class Usuario(AbstractUserRole):
    avaible_permissions = {
        'sugerir_receita' : True,
       
    }
