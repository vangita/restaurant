from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=50)
    cover_photo = models.ImageField(upload_to='restaurants/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MainCategory(models.Model):
    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='main_categories')

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    cover_photo = models.ImageField(upload_to='subcategories/')
    parent_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Dish(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='dishes/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='dishes')
    ingredients = models.ManyToManyField(Ingredient, related_name='dishes')

    def __str__(self):
        return self.name



