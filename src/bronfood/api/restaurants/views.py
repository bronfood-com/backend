from bronfood.core.restaurants.models import (
    Tag,
    Dish,
    Restaurant,
    Menu,
)
from .serializers import (
    RestaurantSerializer,
    MenuSerializer,
    TagSerializer,
    DishSerializer,
)
from rest_framework import viewsets


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
