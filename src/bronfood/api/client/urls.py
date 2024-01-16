from django.urls import path, re_path
from djoser.views import TokenDestroyView

from .views import (ClientChangePasswordView,
                    ClientConfirmationView, ClientProfileView,
                    ClientRegistrationView, CustomTokenCreateView,
                    ClientDataToRegistrationView,  # перенаправление данных
                    ClientDataToProfileView,
                    )

app_name = 'client'

urlpatterns = [
    path('profile/', ClientProfileView.as_view(), name='profile'),
#     path('change_password/request/',
#          ClientChangePasswordRequestView.as_view(),
#          name='change_password_request'),
#     path('change_password/confirmation/',
#          ClientChangePasswordConfirmationView.as_view(),
#          name='change_password_confirmation'),
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
    path('data_to_signup/', ClientDataToRegistrationView.as_view(), name="data_to_signup"),
    path('data_to_profile/', ClientDataToProfileView.as_view(), name="data_to_profile"),
]