from bronfood.core.restaurants.models import Restaurant, Menu
from .serializers import RestaurantSerializer, MenuSerializer
from rest_framework import viewsets


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
