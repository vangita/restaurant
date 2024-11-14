from django.contrib import admin
from .models import Restaurant, SubCategory, Dish, Ingredient, MainCategory

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(MainCategory)
admin.site.register(SubCategory)
admin.site.register(Dish)
admin.site.register(Ingredient)
