from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bronfood.api.restaurant_admin.views import RestaurantAdminViewSet

router = DefaultRouter()
router.register(r'', RestaurantAdminViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
