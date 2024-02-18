# custom auth_backends.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class PhoneBackend(BaseBackend):
    """
    Работает для клиента и владельца ресторана, проверка пароля и телефона.
    """

    def authenticate(self, request, username=None, password=None):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
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
    """Работает для админа ресторана, проверка пароля и юзернэйм."""
