from rest_framework import serializers

from bronfood.core.payment_requisites.models import PaymentRequisites


class PaymentRequisitesCreateSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = PaymentRequisites
        fields = ['card_number', 'cardholder_name', 'expiration_data', 'cvv']
        extra_kwargs = {
            'card_number': {'required': True},
            'cardholder_name': {'required': True},
            'expiration_data': {'required': True},
            'cvv': {'required': True},
        }

    def create(self, validated_data, **kwargs):
        return PaymentRequisites.objects.create(**validated_data)


class PaymentRequisitesUpdateSerializer(serializers.ModelSerializer):
    # cvv = serializers.SerializerMethodField()

    class Meta:
        model = PaymentRequisites
        fields = ['card_number', 'cardholder_name', 'expiration_data', 'cvv']
        extra_kwargs = {
            'card_number': {'required': False},
            'cardholder_name': {'required': False},
            'expiration_data': {'required': False},
            'cvv': {'required': False},
        }

    def update(self, instance: PaymentRequisites, validated_data):
        instance.card_number = validated_data.get(
            'card_number', instance.card_number)
        instance.cardholder_name = validated_data.get(
            'cardholder_name', instance.cardholder_name)
        instance.expiration_data = validated_data.get(
            'expiration_data', instance.expiration_data
        )
        instance.cvv = validated_data.get(
            'cvv', instance.cvv
        )
        instance.save()
        return instance

    # def get_cvv(self, obj):
    #     # Здесь вы можете вернуть "Данные не доступны" или что-то еще
    #     return "Данные не доступны"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Удаление поля 'cvv' из представления данных
        data.pop('cvv', None)
        return data
