from .models import RestaurantOwner
from rest_framework import serializers


class RestaurantOwnerSerializer(serializers.ModelSerializer):
    """Сериализатор владельца заведения."""
    class Meta:
        model = RestaurantOwner
        fields = (
            'id',
            'email',
            'username',
            'phone',
        )
