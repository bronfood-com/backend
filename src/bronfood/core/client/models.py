from django.db import models
from bronfood.core.useraccount.models import UserAccount


class ClientManager(models.Manager):
    def create_user(self, phone, username, password=None):
        if not phone or len(phone) <= 0:
            raise ValueError("Phone field is required !")
        if not username or len(username) <= 0:
            raise ValueError("Username field is required !")
        if not password:
            raise ValueError("Password is must !")
        user = self.model(
            phone=phone,
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
        return super().save(*args, **kwargs)
