# custom auth_backends.py

from django.contrib.auth.backends import BaseBackend
from .models import CustomUser


class PhoneBackend(BaseBackend):
    """
    Работает для клиента и владельца ресторана, проверка пароля и телефона.
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                return None
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None


class UsernameBackend(BaseBackend):
    """Работает для админа ресторана, проерка пароля и юзернэйм."""
