from django.urls import path, re_path
from djoser.views import TokenDestroyView

from .views import (ClientChangePasswordCompleteView,
                    ClientChangePasswordConfirmationView,
                    ClientChangePasswordRequestView, ClientProfileView,
                    ClientRegistrationView, ClientRequestProfileUpdateView,
                    ClientRequestRegistrationView)

app_name = 'client'

urlpatterns = [
    path('request_to_signup/',
         ClientRequestRegistrationView.as_view(),
         name="request_to_signup"),
    path('signup/',
         ClientRegistrationView.as_view(),
         name='signup'),
    path('change_password/request/',
         ClientChangePasswordRequestView.as_view(),
         name='change_password_request'),
    path('change_password/confirmation/',
         ClientChangePasswordConfirmationView.as_view(),
         name='change_password_confirmation'),
    path('change_password/complete/',
         ClientChangePasswordCompleteView.as_view(),
         name='change_password_complete'),
    path('profile/update_request/',
         ClientRequestProfileUpdateView.as_view(),
         name='profile_update_request'),
    path('profile/', ClientProfileView.as_view(), name='profile'),
]

# Token
urlpatterns += [
    re_path(r"^signout/?$", TokenDestroyView.as_view(), name="signout"),
]
