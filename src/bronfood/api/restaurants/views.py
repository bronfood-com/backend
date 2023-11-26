from bronfood.core.restaurants.models import (
    Tag, Dishes, CategoryDishes, Restaurant, Menu)
from .serializers import (
    RestaurantSerializer,
    MenuSerializer,
    TagSerializer,
    DishesSerializer,
    CategoryDishesSerializer,
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


class DishesViewSet(viewsets.ModelViewSet):
    queryset = Dishes.objects.all()
    serializer_class = DishesSerializer


class CategoryDishesViewSet(viewsets.ModelViewSet):
    queryset = CategoryDishes.objects.all()
    serializer_class = CategoryDishesSerializer