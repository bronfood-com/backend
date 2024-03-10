from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RestaurantOwnerViewSet

app_name = 'client'

router = DefaultRouter()
router.register('owner', RestaurantOwnerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
