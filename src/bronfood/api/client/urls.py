from django.urls import path, re_path
from djoser.views import TokenDestroyView

from .views import (
                    # ClientChangePasswordCompleteView,
                    ClientProfileView,
                    ClientRegistrationView,
                    CustomTokenCreateView,
                    ClientRequestRegistrationView,
                    ClientChangePasswordRequestView,
                    ClientChangePasswordConfirmationView,
                    ClientRequestProfileUpdateView
                    )

app_name = 'client'

urlpatterns = [
    path('request_to_signup/',  # создание клиента
         ClientRequestRegistrationView.as_view(),
         name="request_to_signup"),
    path('signup/',  # активация клиента и авторизация
         ClientRegistrationView.as_view(),
         name='signup'),
    path('change_password/request/',  # запрос на смену пароля
         ClientChangePasswordRequestView.as_view(),
         name='change_password_request'),
    path('change_password/confirmation/', # подтверждение
         ClientChangePasswordConfirmationView.as_view(),
         name='change_password_confirmation'),
     # path('change_password/complete/',
     #     ClientChangePasswordCompleteView.as_view(),
     #     name='change_password_compelete'),
     path('profile/update_request/',
          ClientRequestProfileUpdateView.as_view(),
          name='profile_update_request'),
     path('profile/', ClientProfileView.as_view(), name='profile'),
     # path('change_password/',
     #     ClientChangePasswordCompleteView.as_view(),
     #     name='change_password'),
]

# Token
urlpatterns += [
    re_path(r"^signout/?$", TokenDestroyView.as_view(), name="signout"),
    re_path(r"^signin/?$", CustomTokenCreateView.as_view(), name="signin"),
]
