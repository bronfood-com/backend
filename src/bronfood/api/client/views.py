from rest_framework import viewsets

from bronfood.core.restaurant_owner.models import RestaurantOwner
from .serializers import RestaurantOwnerSerializer


class RestaurantOwnerViewSet(viewsets.ModelViewSet):
    """Набор представлений для владельца заведения."""
    queryset = RestaurantOwner.objects.all()
    serializer_class = RestaurantOwnerSerializer
