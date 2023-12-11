from rest_framework import viewsets

from .models import RestaurantOwner
from .serializers import RestaurantOwnerSerializer


class RestaurantOwnerViewSet(viewsets.ModelViewSet):
    """Набор представлений для владельца заведения."""
    queryset = RestaurantOwner.objects.all()
    serializer_class = RestaurantOwnerSerializer
