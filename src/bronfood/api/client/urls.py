from django.urls import path
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
]
