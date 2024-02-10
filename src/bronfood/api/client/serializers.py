from django.contrib.auth import authenticate
from django.core import validators
from rest_framework import serializers

from bronfood.core.client.models import Client
from bronfood.core.useraccount.models import UserAccount, UserAccountTempData
from bronfood.core.useraccount.validators import (  # ConfirmationValidator,
    FullnameValidator, KazakhstanPhoneNumberValidator, validate_password)


class ClientRequestRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериалайзер данных клиента.
    - password
    - phone
    - fullname

    Предусматривает создание объекта клиента.
    Обеспечивает кодирование пароля перед сохранением в БД.
    """
    password = serializers.CharField(
        write_only=True,
        validators=[
            validators.MinLengthValidator(4),
            validators.MaxLengthValidator(20),
            validate_password,
        ]
    )
    phone = serializers.CharField(
        validators=[KazakhstanPhoneNumberValidator()]
    )
    fullname = serializers.CharField(
        validators=[FullnameValidator()]
    )

    class Meta:
        model = Client
        fields = ['password', 'phone', 'fullname']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])
        return user

    def validate(self, data):
        if Client.objects.filter(phone=data.get('phone')).exists():
            raise serializers.ValidationError(
                'Phone number is already exists.'
            )
        return data


class TempDataSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления объекта клиента.
    """
    password = serializers.CharField(
        required=False,
        validators=[
            validators.MinLengthValidator(4),
            validators.MaxLengthValidator(20),
            validate_password,
        ]
    )
    password_confirm = serializers.CharField(
        required=False,
    )
    fullname = serializers.CharField(
        required=False,
        validators=[FullnameValidator()]
    )
    phone = serializers.CharField(
        required=False,
        validators=[KazakhstanPhoneNumberValidator()]
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=UserAccount.objects.all(),
        required=True)

    class Meta:
        model = UserAccountTempData
        fields = ['password',
                  'password_confirm',
                  'fullname',
                  'phone',
                  'user'
                  ]

    def create(self, validated_data):
        user = validated_data.pop('user')
        temp_data = UserAccountTempData.objects.create_temp_data(
            user=user, **validated_data)
        return temp_data

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password or password_confirm:
            if password != password_confirm:
                raise serializers.ValidationError(
                    'Рasswords do not match')
        if Client.objects.filter(phone=data.get('phone')).exists():
            raise serializers.ValidationError(
                'Phone number exist'
            )
        password_confirm = data.pop('password_confirm')
        return data


class ClientLoginSerializer(serializers.Serializer):
    """
    Сериализатор для входа клиента.
    """
    phone = serializers.CharField(
        validators=[KazakhstanPhoneNumberValidator()]
    )
    password = serializers.CharField(
        validators=[
            validators.MinLengthValidator(4),
            validators.MaxLengthValidator(20),
            validate_password,
        ],
        write_only=True,
    )

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        if phone and password:
            user = authenticate(phone=phone, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.'
                )
        else:
            raise serializers.ValidationError(
                'Both phone and password are required fields.'
            )
        return data


class ClientUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления профиля клиента.
    """
    password = serializers.CharField(
        required=False,
        # validators=[PasswordValidator()]
    )
    phone = serializers.CharField(
        required=False,
        validators=[KazakhstanPhoneNumberValidator()]
    )
    fullname = serializers.CharField(
        required=False,
        validators=[FullnameValidator()]
    )

    class Meta:
        model = Client
        fields = ['password',
                  'phone',
                  'fullname']
