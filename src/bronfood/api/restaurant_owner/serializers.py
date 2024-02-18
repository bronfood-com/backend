from rest_framework import serializers
from bronfood.core.restaurant_owner.models import RestaurantOwner


class RestaurantOwnerSerializer(serializers.ModelSerializer):
    """Сериализатор владельца заведения."""
    class Meta:
        model = RestaurantOwner
        fields = '__all__'
