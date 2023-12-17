from rest_framework import serializers
from bronfood.core.client.models import Client
from django.contrib.auth import authenticate
from bronfood.core.useraccount.validators import OnlyDigitsValidator


class ClientPasswordResetSerializer(serializers.Serializer):
    """
    Сериализатор для восстановления пароля клиента.
    Осуществляется на основе телефона и нового пароля.
    """
    phone = serializers.CharField(max_length=18,
                                  validators=[OnlyDigitsValidator()])
    new_password = serializers.CharField(write_only=True)


class ClientSerializer(serializers.ModelSerializer):
    """
    Сериалайзер модели клиента.
    Обеспечивает кодирование пароля перед сохранением в БД.
    """
    password = serializers.CharField(
        write_only=True,
    )
    phone = serializers.CharField(
        validators=[OnlyDigitsValidator()]
    )

    class Meta:
        model = Client
        fields = ['password', 'phone', 'username']

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
    password = serializers.CharField(required=False)
    phone = serializers.IntegerField(required=False,
                                     validators=[OnlyDigitsValidator()])
    username = serializers.CharField(required=False)

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
    phone = serializers.CharField(validators=[OnlyDigitsValidator()])
    password = serializers.CharField(write_only=True)

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


class ClientObjAndCookieSerializer(serializers.Serializer):
    """
    Предоставление данных о клиенте и сессии.
    """
    session_key = serializers.CharField()
    phone = serializers.CharField()
    username = serializers.CharField()
