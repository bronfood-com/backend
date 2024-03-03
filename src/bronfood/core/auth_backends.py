# custom auth_backends.py

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class PhoneBackend(BaseBackend):
    """
    Работает для клиента и владельца ресторана, проверка пароля и телефона.
    """

    def authenticate(self, request, phone=None, password=None, **kwargs):
        if phone is None:
            phone = kwargs.get(User.USERNAME_FIELD)
        if phone is None or password is None:
            return
        try:
            user = User._default_manager.get_by_natural_key(phone)
        except User.DoesNotExist:
            User().set_password(password)
        else:
            if (user.check_password(password) and
                    self.user_can_authenticate(user)):
                return user

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        return user.status == "Confirmed"

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class UsernameBackend(BaseBackend):
    """Работает для админа ресторана, проверка пароля и юзернэйм."""

    def authenticate(self, request, phone, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                return None
        except user.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
