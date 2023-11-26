from bronfood.core.restaurants.models import (
    Restaurant,
    Menu,
    Dishes,
    Tag,
    CategoryDishes,
)
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
        )


class DishesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = (
            'id',
            'name',
            'price',
            'description',
            'pic',
        )


class CategoryDishesSerializer(serializers.ModelSerializer):
    dishes = DishesSerializer(many=True, read_only=True)

    class Meta:
        model = CategoryDishes
        fields = (
            'id',
            'name',
            'dishes',
        )


class MenuSerializer(serializers.ModelSerializer):
    dishes = DishesSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = (
            'id',
            'is_active',
            'is_archived',
            'rating',
            'pic',
            'dishes',
        )


class RestaurantSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(many=True, read_only=True)
    tag = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = (
            'id',
            'title',
            'adress',
            'description',
            'pic',
            'from_work',
            'to_work',
            'type_of_restaurant',
            'tags',
            'is_canceled',
            'time_to_cancel',
            'menu',
            'tag',
        )
