from rest_framework import serializers
from bronfood.core.restaurant_admin.models import RestaurantAdmin


class RestaurantAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantAdmin
        fields = '__all__'
