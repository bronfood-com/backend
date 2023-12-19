from rest_framework import serializers
from bronfood.core.client.models import Client
from django.contrib.auth import authenticate
from bronfood.core.useraccount.validators import (
    KazakhstanPhoneNumberValidator,
    PasswordValidator,
    UsernameValidator,
    ConfirmationValidator
)


class ClientPasswordResetSerializer(serializers.Serializer):
    """
    Сериализатор для восстановления пароля клиента.
    Осуществляется на основе телефона и нового пароля.
    """
    phone = serializers.CharField(
        validators=[KazakhstanPhoneNumberValidator()]
    )
    new_password = serializers.CharField(
        write_only=True,
        validators=[PasswordValidator()]
    )


class ClientSerializer(serializers.ModelSerializer):
    """
    Сериалайзер модели клиента.
    Обеспечивает кодирование пароля перед сохранением в БД.
    """
    password = serializers.CharField(
        write_only=True,
        validators=[PasswordValidator()]
    )
    phone = serializers.CharField(
        validators=[KazakhstanPhoneNumberValidator()]
    )

    class Meta:
        model = Client
        fields = ['password', 'phone', ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            # Обеспечивает кодирование пароля перед сохранением в БД.
            user.set_password(password)
            user.save(update_fields=['password'])
        return user


class ClientUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления объекта клиента.
    """
    password = serializers.CharField(
        required=False,
        validators=[PasswordValidator()]
    )
    phone = serializers.IntegerField(
        required=False,
        validators=[KazakhstanPhoneNumberValidator()]
    )
    username = serializers.CharField(
        required=False,
        validators=[UsernameValidator()]
    )

    class Meta:
        model = Client
        fields = ['password', 'phone', 'username']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class ClientLoginSerializer(serializers.Serializer):
    """
    Сериализатор для входа клиента.
    """
    phone = serializers.CharField(
        validators=[KazakhstanPhoneNumberValidator()]
    )
    password = serializers.CharField(
        validators=[PasswordValidator()],
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


class ClientResponseSerializer(serializers.Serializer):
    """
    Предоставление данных о клиенте.
    """
    phone = serializers.CharField()


class ConfirmationSerializer(serializers.Serializer):
    """
    Код подтверждения.
    """
    confirmation_code = serializers.CharField(
        validators=[ConfirmationValidator()],
        write_only=True,
    )
