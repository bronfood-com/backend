from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (AbstractUser)
from django.utils.translation import gettext_lazy as _


class RestaurantOwner(AbstractUser):
    """
    Модель клиента RestaurantOwner
    обязательные поля:
        "имя фамилия",
        "телефон",
        "пароль"
    """
    username = models.CharField(
        "username",
        max_length=150,
        validators=[UnicodeUsernameValidator(), ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        "email",
        max_length=255,
        blank=True,
        null=True,
        unique=True,
    )
    phone = models.CharField(
        "phone",
        max_length=15,
        unique=True,
    )
    user = models.OneToOneField(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='restaurant_owner'
    )
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username', 'email', 'phone']

    class Meta:
        verbose_name = 'Владелец'
        verbose_name_plural = 'Владельцы'
        ordering = ('id',)

    def __str__(self):
        return self.username
