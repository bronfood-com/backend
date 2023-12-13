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
    path('signup/', ClientRegistrationView.as_view(), name='signup'),
    path('signin/', ClientLoginView.as_view(), name='signin'),
    path('signout/', ClientLogoutView.as_view(), name='signout'),
    path('info/', ClientInfoView.as_view(), name='info'),
    path('password_reset/',
         ClientPasswordResetView.as_view(),
         name='password_reset'),
    path('', include('rest_framework.urls')),
]
