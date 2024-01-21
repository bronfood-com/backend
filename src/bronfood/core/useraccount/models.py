from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .validators import (FullnameValidator,
                         KazakhstanPhoneNumberValidator)


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


class TempUserAccountData(models.Model):
    """
    Временное хранение данных пользователя.
    """

    new_password = models.CharField(
        max_length=128,
        null=True)
    user = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name='temp'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user + self.created_at