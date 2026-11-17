# recipes/tasks.py
import re
import requests
from celery import shared_task
from .models import Recipe

def _parse_ingredients(meal):
    ingredients = []
    for i in range(1, 21):
        name = (meal.get(f"strIngredient{i}") or "").strip()
        measure = (meal.get(f"strMeasure{i}") or "").strip()
        if name:
            match = re.match(r"^([\d.,/]+)\s*(.*)$", measure)
            if match:
                raw_num, unit_and_rest = match.groups()
                try:
                    qty = float(raw_num.split("/")[0]) / float(raw_num.split("/")[1]) if "/" in raw_num else float(raw_num.replace(",", "."))
                except ValueError:
                    qty = None
                desc = f"{unit_and_rest} {name}".strip()
            else:
                qty = None
                desc = f"{measure} {name}".strip()

            ingredients.append({
                "qty": qty,
                "display_qty": raw_num if qty else "",
                "description": desc,
            })
    return ingredients

 # busca receitas na TheMealDB em segundo plano e salva no banco local.
@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def sync_catalog_task(self, search_term=""):
   
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={search_term}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        meals = response.json().get("meals") or []
    except requests.RequestException as exc:
        raise self.retry(exc=exc)

    count = 0
    for meal in meals:
        Recipe.objects.update_or_create(
            meal_id=meal["idMeal"],
            defaults={
                "title": meal.get("strMeal", ""),
                "category": meal.get("strCategory") or "Geral",
                "area": meal.get("strArea") or "Internacional",
                "thumb_url": meal.get("strMealThumb", ""),
                "instructions": meal.get("strInstructions", ""),
                "ingredients_json": _parse_ingredients(meal),
            }
        )
        count += 1

    return f"Sucesso: {count} receitas sincronizadas para o termo '{search_term}'."