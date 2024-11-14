from rest_framework import serializers
from django.contrib.auth.models import User
from menu.models import MainCategory, Restaurant, SubCategory, Ingredient, Dish


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class DishSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Dish
        fields = ['name', 'photo', 'ingredients']

    def create(self, validated_data):
        ingredients_data = self.context.get('ingredients', [])
        dish = super().create(validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(dish=dish, **ingredient_data)
        return dish

class SubCategorySerializer(serializers.ModelSerializer):
    parent_category_name = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = ['parent_category_name','name', 'cover_photo']
    def get_parent_category_name(self, obj):
        return obj.parent_category.name



class MainCategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = MainCategory
        fields = ['id', 'name', 'restaurant', 'subcategories']

class MainCategoryMinimalSerializer(MainCategorySerializer):
    class Meta:
        model = MainCategory
        fields = ['id', 'name']


class RestaurantSerializer(serializers.ModelSerializer):
    main_categories = MainCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone_number', 'cover_photo', 'main_categories']
        read_only_fields = ['owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class RestaurantMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
