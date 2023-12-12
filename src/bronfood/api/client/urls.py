# Создать эдпоинты для клиента в api/client (views, serializers, urls)
# интегрировать их в основное приложение проекта (пока пустые)
from django.urls import path, include
from .views import (ClientRegistrationView,
                    ClientInfoView,
                    ClientLoginView,
                    ClientLogoutView,
                    ClientPasswordResetView)


app_name = 'client'

urlpatterns = [
    path('registration/', ClientRegistrationView.as_view(), name='index'),
    path('my_login/', ClientLoginView.as_view(), name='my_login'),
    path('my_logout/', ClientLogoutView.as_view(), name='my_logout'),
    path('info/', ClientInfoView.as_view(), name='info'),
    path('password_recovery/',
         ClientPasswordResetView.as_view(),
         name='password_recovery'),
    path('', include('rest_framework.urls')),
]
