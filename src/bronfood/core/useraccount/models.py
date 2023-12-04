from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .validators import CustomUnicodeUsernameValidator


class UserAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email or len(email) <= 0:
            raise ValueError("Email field is required !")
        if not username or len(username) <= 0:
            raise ValueError("Username field is required !")
        if not password:
            raise ValueError("Password is must !")

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    """
    Общая модель для пользовательского аккаунта.
    """
    class Types(models.TextChoices):
        CLIENT = "CLIENT", "client"
        OWNER = "OWNER", "owner"

    type = models.CharField(max_length=8, choices=Types.choices,
                            default=Types.CLIENT)
    username = models.CharField(max_length=200,
                                validators=[CustomUnicodeUsernameValidator])
    email = models.EmailField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserAccountManager()

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if not self.type or self.type is None:
            self.type = UserAccount.Types.CLIENT
        return super().save(*args, **kwargs)
