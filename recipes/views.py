from django.shortcuts import render, get_object_or_404
import re
import requests
from django.http import Http404
from .models import Recipe
from .tasks import sync_catalog_task

def home(request):
    query = request.GET.get("q", "").strip()
    
    if query:
        meals = Recipe.objects.filter(title__icontains=query)
        # se não encontrou no banco local, manda o Celery buscar na API 
        if not meals.exists():
            sync_catalog_task.delay(query)
    else:
        meals = Recipe.objects.order_by('?')[:12] # aleatoriza quando atualiza
        if not meals.exists():
            sync_catalog_task.delay("")

    return render(request, "recipes/pages/home.html", {
        "meals": meals,
        "query": query,
    })


def recipe(request, id):
    # busca pelo meal_id salvo no banco local
    recipe_obj = get_object_or_404(Recipe, meal_id=str(id))
    
    steps = [
        s.strip() for s in re.split(r"\r?\n+", recipe_obj.instructions)
        if s.strip() and not s.strip().lower().startswith("step ")
    ]

    related_meals = Recipe.objects.filter(category=recipe_obj.category).exclude(id=recipe_obj.id)[:3]

    recipe_data = {
        "id": recipe_obj.meal_id,
        "title": recipe_obj.title,
        "category": recipe_obj.category,
        "area": recipe_obj.area,
        "image": recipe_obj.thumb_url,
        "ingredients": recipe_obj.ingredients_json,
        "steps": steps,
    }

    return render(request, "recipes/pages/recipe.html", {
        "recipe": recipe_data,
        "related_meals": related_meals,
    })

def _parse_meal_data(meal):
    # Normaliza o JSON bruto da TheMealDB para a estrutura do template.
    ingredients = []
    for i in range(1, 21):
        name = (meal.get(f"strIngredient{i}") or "").strip()
        measure = (meal.get(f"strMeasure{i}") or "").strip()
        
        if name:
            # Tenta extrair um número inicial da medida para manter compatível com seu JS (data-q)
            match = re.match(r"^([\d.,/]+)\s*(.*)$", measure)
            if match:
                raw_num, unit_and_rest = match.groups()
                try:
                    # Converte frações simples como "1/2" para float 0.5
                    if "/" in raw_num:
                        num, den = raw_num.split("/")
                        qty = float(num) / float(den)
                    else:
                        qty = float(raw_num.replace(",", "."))
                except ValueError:
                    qty = None
                description = f"{unit_and_rest} {name}".strip()
            else:
                qty = None
                description = f"{measure} {name}".strip()

            ingredients.append({
                "qty": qty,
                "display_qty": raw_num if qty else "",
                "description": description,
            })

    # Divide o texto contínuo de instruções em parágrafos/passos limpos
    raw_instructions = meal.get("strInstructions") or ""
    steps = [
        step.strip() 
        for step in re.split(r"\r?\n+", raw_instructions) 
        if step.strip() and not step.strip().lower().startswith("step ")
    ]

    return {
        "id": meal.get("idMeal"),
        "title": meal.get("strMeal"),
        "category": meal.get("strCategory") or "Geral",
        "area": meal.get("strArea") or "Internacional",
        "image": meal.get("strMealThumb"),
        "youtube": meal.get("strYoutube"),
        "tags": meal.get("strTags").split(",") if meal.get("strTags") else [],
        "ingredients": ingredients,
        "steps": steps,
    }


def recipe_detail(request, meal_id="52772"): 
    url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        raise Http404("Erro ao comunicar com a API de receitas.")

    meals = data.get("meals")
    if not meals:
        raise Http404("Receita não encontrada.")

    recipe = _parse_meal_data(meals[0])

    related_url = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={recipe['category']}"
    related_meals = []
    try:
        rel_res = requests.get(related_url, timeout=5).json()
        all_rel = rel_res.get("meals") or []
        related_meals = [m for m in all_rel if m["idMeal"] != recipe["id"]][:3]
    except requests.RequestException:
        pass

    context = {
        "recipe": recipe,
        "related_meals": related_meals,
    }
    return render(request, "recipes/pages/recipe.html", context)