from django.urls import include, path
from rest_framework import routers

from .restaurants.views import (
    RestaurantViewSet,
    MenuViewSet,
    TagViewSet,
    MealViewSet,
    OrderViewSet,
    OrderedMealViewSet,
    BasketViewSet,
    CoordinatesViewSet,
    ChoiceViewSet,
    FeatureViewSet,
    FavoritesViewSet,
    MealInBasketViewSet,
    RestaurantMeals,
    RestaurantMealDetail,
    UserFavoritesView,
    DeleteUserFavoriteView
)

router = routers.DefaultRouter()
router.register('restaurant', RestaurantViewSet, basename='restaurant')
router.register('menus', MenuViewSet, basename='menu')
router.register('tags', TagViewSet, basename='tag')
router.register('meals', MealViewSet, basename='meal')
router.register('orders', OrderViewSet, basename='order')
router.register('ordered_meals', OrderedMealViewSet, basename='ordered_meal')
router.register('coordinates', CoordinatesViewSet, basename='coordinates')
router.register('choices', ChoiceViewSet, basename='choice')
router.register('features', FeatureViewSet, basename='feature')
router.register('favorites', FavoritesViewSet, basename='favorite')
router.register('meals_in_basket', MealInBasketViewSet, basename='meal_in_basket')

urlpatterns = [
    path('', include(router.urls)),
    path('restaurant/<int:pk>/meal', RestaurantMeals.as_view(), name='restaurant-meals'),
    path('restaurant/<int:restaurant_id>/meal/<int:meal_id>', RestaurantMealDetail.as_view(), name='restaurant-meal-detail'),
    path('user/<int:user_id>/favorites', UserFavoritesView.as_view(), name='user-favorites'),
    path('user/<int:user_id>/favorites/<int:restaurant_id>', DeleteUserFavoriteView.as_view(), name='delete-user-favorite'),
    path('basket/', BasketViewSet.as_view({'get': 'list'}), name='api_basket_get'),
    path('basket/clear/', BasketViewSet.as_view({'delete': 'clear'}), name='basket-clear'),
    path('basket/add_meal/', BasketViewSet.as_view({'post': 'add_meal'}), name='basket-add-meal'),
    path('basket/<mealId>', BasketViewSet.as_view({'delete': 'remove_meal'}), name='basket-delete-meal'),
]
