from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .validators import (FullnameValidator,
                         KazakhstanPhoneNumberValidator)
import random
from bronfood.core.constants import LETTERS_AND_DIGITS, TEMP_DATA_CODE_LENGTH

class UserAccountManager(BaseUserManager):
    def create_user(self, phone, username, password=None):
        user = self.model(
            phone=phone,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, password):
        user = self.create_user(
            phone=phone,
            username=username,
            password=password
        )
        user.role = UserAccount.Role.ADMIN
        user.status = UserAccount.Status.CONFIRMED
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    """
    Общая модель для пользовательского аккаунта.
    """
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "admin"
        CLIENT = "CLIENT", "client"
        OWNER = "OWNER", "owner"
        RESTAURANT_ADMIN = "RESTAURANT_ADMIN", "restaurant_admin"

    class Status(models.IntegerChoices):
        UNCONFIRMED = 0, 'Unconfirmed'
        CONFIRMED = 1, 'Confirmed'
        BLOCKED = 2, 'Blocked'

    role = models.CharField(max_length=16, choices=Role.choices,
                            default=Role.CLIENT)
    # TODO необходимо добавить валидатор для username
    username = models.CharField(max_length=40)
    fullname = models.CharField(max_length=40,
                                validators=[FullnameValidator])
    phone = models.CharField(max_length=18,
                             unique=True,
                             validators=[KazakhstanPhoneNumberValidator])
    status = models.SmallIntegerField(choices=Status.choices,
                                      default=Status.UNCONFIRMED)
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username"]

    objects = UserAccountManager()

    def __str__(self):
        return str(self.phone)

    def has_perm(self, perm, obj=None):
        return self.role == UserAccount.Role.ADMIN

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if not self.role or self.role is None:
            self.role = UserAccount.Role.CLIENT
        return super().save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.role == UserAccount.Role.ADMIN

    @property
    def is_superuser(self):
        return self.role == UserAccount.Role.ADMIN


class UserAccountTempData(models.Model):
    """
    Временное хранение данных пользователя.
    """
    temp_data_code = models.CharField(
        max_length=TEMP_DATA_CODE_LENGTH,
    )
    new_password = models.CharField(
        max_length=128,
        null=True)
    user = models.OneToOneField(
        UserAccount,
        on_delete=models.CASCADE,
        related_name='user_account_temp_data',
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    new_fullname = models.CharField(
        max_length=40,
        validators=[FullnameValidator],
        null=True
    )
    new_phone = models.CharField(
        max_length=18,
        validators=[KazakhstanPhoneNumberValidator],
        null=True
    )
    

    @classmethod
    def get_unique_data_code(cls) -> str:
        """получение уникального кода"""
        rand_string = ''.join(random.choices(
            population=LETTERS_AND_DIGITS,
            k=TEMP_DATA_CODE_LENGTH)
        )
        # возврат только уникального результата
        if not cls.objects.filter(temp_data_code=rand_string).exists():
            return rand_string
        return cls.get_unique_data_code()
    
    def __str__(self):
        return self.temp_data_code