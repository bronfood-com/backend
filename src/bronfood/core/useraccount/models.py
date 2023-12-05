from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .validators import CustomUnicodeUsernameValidator


class UserAccountManager(BaseUserManager):
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

    def create_superuser(self, phone, username, password):
        user = self.create_user(
            phone=phone,
            username=username,
            password=password
        )
        user.role = UserAccount.Role.ADMIN
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    """
    Общая модель для пользовательского аккаунта.
    """
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "admin"
        STAFF = "STAFF", "staff"
        CLIENT = "CLIENT", "client"
        OWNER = "OWNER", "owner"
        RESTAURANT_ADMIN = "RESTAURANT_ADMIN", "restaurant_admin"

    class ActiveStatus(models.IntegerChoices):
        UNCONFIRMED = 1, 'Unconfirmed'
        CONFIRMED = 2, 'Confirmed'
        BLOCKED = 3, 'Blocked'

    role = models.CharField(max_length=8, choices=Role.choices,
                            default=Role.CLIENT)
    username = models.CharField(max_length=200,
                                validators=[CustomUnicodeUsernameValidator])
    phone = models.CharField(max_length=18, unique=True)
    active_status = models.SmallIntegerField(choices=ActiveStatus.choices,
                                             default=ActiveStatus.UNCONFIRMED)
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username"]

    objects = UserAccountManager()

    def __str__(self):
        return str(self.phone)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if not self.role or self.role is None:
            self.role = UserAccount.Role.CLIENT
        return super().save(*args, **kwargs)
