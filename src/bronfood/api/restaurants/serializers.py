from bronfood.core.restaurants.models import Restaurant, Menu
from rest_framework import serializers


class RestaurantSerializer(serializers.ModelSerializer):
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
        )


class MenuSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(many=False, read_only=True)

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
            'restaurant',
        )
