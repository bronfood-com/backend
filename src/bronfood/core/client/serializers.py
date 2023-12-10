from rest_framework import serializers
from .models import Client
from django.contrib.auth import authenticate


# class OwnerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Owner
#         fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    """
    Сериалайзер модели клиента.
    Обеспечивает кодирование пароля перед сохранением в БД.
    """
    password = serializers.CharField(
        # write_only=True
    )

    class Meta:
        model = Client
        fields = ['password', 'phone', 'username']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])
        return user


class UpdateClientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления объекта клиента.
    """
    password = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = Client
        fields = ['password', 'email']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class ClientLoginSerializer(serializers.Serializer):
    """
    Сериализатор для входа клиента.
    """
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        if phone and password:
            user = authenticate(phone=phone, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Both phone and password are required fields.')

        return data