from django.urls import path, re_path
from .views import (ClientRegistrationView,
                    ClientProfileView,
                    ClientChangePasswordView,
                    ClientConfirmationView,
                    ClientChangePasswordRequestView,
                    ClientChangePasswordConfirmationView,
                    ClientRegistrationView,
                    CustomTokenCreateView
                    )
from djoser.views import TokenDestroyView


app_name = 'client'

urlpatterns = [
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
    