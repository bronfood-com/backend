from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, phone, password=None, is_owner=False,
                    **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        if not password:
            raise ValueError('The Password field must be set')

        user = self.model(
            username=username,
            phone=phone,
            is_owner=is_owner,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone, password=None, is_owner=False,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, phone, password, is_owner,
                                **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя

    обязательные поля
    - username
    - phone
    - password
    """
    class Status(models.IntegerChoices):
        CLIENT = 0, 'Клиент'
        OWNER = 1, 'Владелец точки питания'

    # TODO пока дефолтный, заменю на коректный допускающий прабел
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        "username",
        max_length=150,
        validators=[username_validator],
    )
    # TODO УТОЧНИТЬ потребуется ли поле с почтой? (отправлять чеки об оплате?)
    email = models.EmailField(
        "email address",
        max_length=255,
        blank=True,
        null=True,
        unique=True,
    )
    # TODO подключить валидатор на телефон
    phone = models.CharField(
        "phone",
        max_length=15,
        unique=True,
    )
    date_joined = models.DateTimeField(
        "date joined",
        auto_now_add=True,
    )
    # поле для флага на получение смс
    is_verified = models.BooleanField(
        "verify status",
        default=False,
    )
    is_staff = models.BooleanField(
        "staff status",
        default=False,
    )
    is_active = models.BooleanField(
        "active status",
        default=True,
    )
    is_owner = models.BooleanField(
        "owner status",
        choices=Status.choices,
        default=Status.CLIENT
    )

    REQUIRED_FIELDS = ['username', 'password']
    USERNAME_FIELD = 'phone'

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} {self.phone}"
