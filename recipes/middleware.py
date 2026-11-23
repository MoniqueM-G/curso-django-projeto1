# middleware para rastrear as receitas vistas recentemente

class RecipeHistory:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        # Executa a view para garantir que a página existe (não deu erro 404 page not found)
        response = self.get_response(request)
        if response.status_code == 200 and request.path.startswith('/recipes/'):
            partes = request.path.strip('/').split('/')
           
            if len(partes) == 2 in partes[1].isdigit():
                recipe_id = int(partes[1])
                historico = request.session.get('receitas_vistas',[])
                if recipe_id in historico:
                    historico.remove(recipe_id)
                historico.insert(0,recipe_id)
                request.session['receitas_vistas'] = historico[:5]
        return response