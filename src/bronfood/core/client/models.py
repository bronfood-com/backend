from django.db import models
from bronfood.core.useraccount.models import UserAccount


class ClientManager(models.Manager):
    def create_user(self, email, username, password=None):
        if not email or len(email) <= 0:
            raise ValueError("Email field is required !")
        if not username or len(username) <= 0:
            raise ValueError("Username field is required !")
        if not password:
            raise ValueError("Password is must !")
        email = email.lower()
        user = self.model(
            email=email,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(type=UserAccount.Types.CLIENT)
        return queryset


class Client(UserAccount):
    """ Модель Клиента"""
    class Meta:
        proxy = True
    objects = ClientManager()

    def save(self, *args, **kwargs):
        self.type = UserAccount.Types.CLIENT
        self.is_client = True
        return super().save(*args, **kwargs)
