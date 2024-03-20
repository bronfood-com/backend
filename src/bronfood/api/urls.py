from django.urls import include, path
from rest_framework import routers

from .restaurants.views import (
    RestaurantViewSet,
    MenuViewSet,
    TagViewSet,
    DishViewSet,
)

router = routers.DefaultRouter()
router.register('restaurants', RestaurantViewSet)
router.register('menus', MenuViewSet)
router.register('tags', TagViewSet)
router.register('dishes', DishViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
