from .models import Recipe

def recipe_history(request):
    recent_ids = request.session.get('recent_recipes',[])

    if not recent_ids:
        return {'recent_recipes': []}

    ids_to_text = [str(i) for i in recent_ids]

    recipes = Recipe.objects.filter(meal_id__in=ids_to_text)

    sorted_recipes = sorted(
        recipes,
        key=lambda r: ids_to_text.index(r.meal_id)
    )

    return {'recent_recipes': sorted_recipes}