from django.urls import path, re_path
from djoser.views import TokenDestroyView

from .views import (ClientChangePasswordView,
                    ClientConfirmationView, ClientProfileView,
                    ClientRegistrationView, CustomTokenCreateView,
                    ClientRequestSmsForSignupView,
                    ClientRequestSmsForProfileView,
                    )

app_name = 'client'

urlpatterns = [
    path('profile/', ClientProfileView.as_view(), name='profile'),
    path('change_password/',
         ClientChangePasswordView.as_view(),
         name='change_password'),
    path('confirmation/',
         ClientConfirmationView.as_view(),
         name='confirmation'),
    path('signup/',
         ClientRegistrationView.as_view(),
         name='signup')

]

# Token
urlpatterns += [
    re_path(r"^signout/?$", TokenDestroyView.as_view(), name="signout"),
    re_path(r"^signin/?$", CustomTokenCreateView.as_view(), name="signin"),
]

# Redirection
urlpatterns += [
    path('signup/request_sms/',
         ClientRequestSmsForSignupView.as_view(),
         name="request_sms_for_signup"),
    path('profile/request_sms/',
         ClientRequestSmsForProfileView.as_view(),
         name="request_sms_for_profile"),
]
