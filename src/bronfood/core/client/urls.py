from django.urls import path
from .views import CustomUserViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include

app_name = "client"

router = DefaultRouter()
router.register('client', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
