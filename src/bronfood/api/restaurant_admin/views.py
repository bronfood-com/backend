from rest_framework import viewsets
from bronfood.core.restaurant_admin.models import RestaurantAdmin
from bronfood.api.restaurant_admin.serializers import RestaurantAdminSerializer


class RestaurantAdminViewSet(viewsets.ModelViewSet):
    queryset = RestaurantAdmin.objects.all()
    serializer_class = RestaurantAdminSerializer
