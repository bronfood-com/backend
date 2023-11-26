from django.urls import include, path
from rest_framework import routers

from .restaurants.views import (
    RestaurantViewSet,
    MenuViewSet,
    TagViewSet,
    DishesViewSet,
    CategoryDishesViewSet,
)

router = routers.DefaultRouter()
router.register('restaurants', RestaurantViewSet)
router.register('menus', MenuViewSet)
router.register('tags', TagViewSet)
router.register('dishes', DishesViewSet)
router.register('category-dishes', CategoryDishesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
