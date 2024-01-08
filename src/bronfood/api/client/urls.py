from django.urls import path
from .views import (ClientRegistrationView,
                    ClientProfileView,
                    ClientLoginView,
                    ClientLogoutView,
                    ClientChangePasswordView,
                    ClientConfirmationView,
                    ClientChangePasswordRequestView,
                    ClientChangePasswordConfirmationView)


app_name = 'client'

urlpatterns = [
    path('signup/', ClientRegistrationView.as_view(), name='signup'),
    path('signin/', ClientLoginView.as_view(), name='signin'),
    path('signout/', ClientLogoutView.as_view(), name='signout'),
    path('profile/', ClientProfileView.as_view(), name='profile'),
    path('change_password/request/',
         ClientChangePasswordRequestView.as_view(),
         name='change_password_request'),
    path('change_password/confirmation/',
         ClientChangePasswordConfirmationView.as_view(),
         name='change_password_confirmation'),
    path('change_password/',
         ClientChangePasswordView.as_view(),
         name='change_password_complete'),
    path('confirmation/',
         ClientConfirmationView.as_view(),
         name='confirmation')
]
