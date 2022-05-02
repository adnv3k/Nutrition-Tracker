from django.contrib import admin
from .models import Food, Nutrients, FoodHistory

# Register your models here.
admin.site.register(Food)
admin.site.register(Nutrients)
admin.site.register(FoodHistory)
