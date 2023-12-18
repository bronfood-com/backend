from django.urls import path
from .views import (ClientRegistrationView,
                    ClientProfileView,
                    ClientLoginView,
                    ClientLogoutView,
                    ClientPasswordResetView)


app_name = 'client'

urlpatterns = [
    path('signup/', ClientRegistrationView.as_view(), name='signup'),
    path('signin/', ClientLoginView.as_view(), name='signin'),
    path('signout/', ClientLogoutView.as_view(), name='signout'),
    path('profile/', ClientProfileView.as_view(), name='profile'),
    path('password_reset/',
         ClientPasswordResetView.as_view(),
         name='password_reset'),
]
