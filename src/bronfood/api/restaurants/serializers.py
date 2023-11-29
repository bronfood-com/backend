from bronfood.core.restaurants.models import (
    Restaurant,
    Menu,
    Dishes,
    Tag,
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


class MenuSerializer(serializers.ModelSerializer):
    dishes = DishesSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = (
            'id',
            'is_active',
            'pic',
            'dishes',
        )

    @staticmethod
    def get_menu_pic(obj):
        # Получаем последнее блюдо в меню
        last_dish = obj.dishes.last()

        # Если есть блюдо, возвращаем его фото
        if last_dish:
            return last_dish.pic


class RestaurantSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

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
            'tags',
            'rating',
        )
