from django.db import models


class Recipe(models.Model):
    meal_id = models.CharField(max_length=20, unique=True) 
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    thumb_url = models.URLField(max_length=500)
    instructions = models.TextField()
    ingredients_json = models.JSONField(default=list)  
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title