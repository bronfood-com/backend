from bronfood.core.restaurants.models import Restaurant, Menu
from rest_framework import serializers


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = (
            'id',
            'is_active',
            'is_archived',
            'title',
            'price',
            'description',
            'pic',
        )


class RestaurantSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(many=True, read_only=True)

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
        )
