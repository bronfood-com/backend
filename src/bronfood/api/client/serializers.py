from django.contrib.auth import authenticate
from rest_framework import serializers

from bronfood.core.client.models import Client
from bronfood.core.useraccount.validators import (
    ConfirmationValidator, FullnameValidator, KazakhstanPhoneNumberValidator,
    PasswordValidator)


class ClientChangePasswordRequestSerializer(serializers.Serializer):
    """
    Запрос на смену пароля.
    """
    phone = serializers.CharField(
        validators=[KazakhstanPhoneNumberValidator()]
    )


class ClientChangePasswordConfirmationSerializer(serializers.Serializer):
    """
    Подтверждение по смс для смены пароля.
    """
    phone = serializers.CharField()
    confirmation_code = serializers.CharField(
        validators=[ConfirmationValidator()],
        write_only=True,
    )


class ClientGetDataRegistrationSerializer(serializers.ModelSerializer):
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
    fullname = serializers.CharField(
        validators=[FullnameValidator()]
    )
    
    class Meta:
        model = Client
        fields = ['password', 'phone', 'fullname']


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
    fullname = serializers.CharField(
        validators=[FullnameValidator()]
    )
    confirmation_code = serializers.CharField(write_only=True)

    class Meta:
        model = Client
        fields = ['password', 'phone', 'fullname', 'confirmation_code']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            # Обеспечивает кодирование пароля перед сохранением в БД.
            user.set_password(password)
            user.save(update_fields=['password'])
        return user


class ClientChangePasswordSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления пароля клиента.
    """
    new_password = serializers.CharField(
        required=False,
        validators=[PasswordValidator()]
    )
    new_password_confirm = serializers.CharField(
        required=False,
        validators=[PasswordValidator()]
    )
    phone = serializers.CharField(
        validators=[KazakhstanPhoneNumberValidator()]
    )
    confirmation_code = serializers.CharField(write_only=True)


    class Meta:
        model = Client
        fields = ['new_password', 
                  'new_password_confirm',
                  'phone',
                  'confirmation_code']

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError(
                'Введенные пароли не совпадают')
        return data

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password', None)
        if new_password:
            instance.set_password(new_password)
        return super().update(instance, validated_data)


class ClientDataToProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления объекта клиента.
    """
    new_password = serializers.CharField(
        required=False,
        validators=[PasswordValidator()]
    )
    new_password_confirm = serializers.CharField(
        required=False,
        validators=[PasswordValidator()]
    )
    fullname = serializers.CharField(
        required=False,
        validators=[FullnameValidator()]
    )

    class Meta:
        model = Client
        fields = ['new_password', 'new_password_confirm', 'fullname']

    def validate(self, data):
        new_password = data.get('new_password')
        new_password_confirm = data.get('new_password_confirm')

        if new_password or new_password_confirm:
            if new_password != new_password_confirm:
                raise serializers.ValidationError(
                    'Введенные пароли не совпадают')
        return data


class ClientUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления объекта клиента.
    """
    new_password = serializers.CharField(
        required=False,
        validators=[PasswordValidator()]
    )
    new_password_confirm = serializers.CharField(
        required=False,
        validators=[PasswordValidator()]
    )
    fullname = serializers.CharField(
        required=False,
        validators=[FullnameValidator()]
    )
    confirmation_code = serializers.CharField(
        write_only=True)

    class Meta:
        model = Client
        fields = ['new_password', 'new_password_confirm', 'fullname', 'confirmation_code']

    def validate(self, data):
        new_password = data.get('new_password')
        new_password_confirm = data.get('new_password_confirm')

        if new_password or new_password_confirm:
            if new_password != new_password_confirm:
                raise serializers.ValidationError(
                    'Введенные пароли не совпадают')
        return data

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password', None)
        if new_password:
            instance.set_password(new_password)
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
    fullname = serializers.CharField()


class ConfirmationSerializer(serializers.Serializer):
    """
    Код подтверждения.
    """
    confirmation_code = serializers.CharField(
        validators=[ConfirmationValidator()],
        write_only=True,
    )

class ClientLoginSerializer(serializers.Serializer):
    """
    Предоставление данных после регистрации клиента.
    """
    phone = serializers.CharField()
    fullname = serializers.CharField()
    auth_token = serializers.CharField()
