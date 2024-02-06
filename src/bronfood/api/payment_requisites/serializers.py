import re
from rest_framework import serializers

from bronfood.core.payment_requisites.models import PaymentRequisites


class PaymentRequisitesCreateSerializer(
    serializers.ModelSerializer
):
    card_number = serializers.CharField()

    class Meta:
        model = PaymentRequisites
        fields = ['card_number', 'cardholder_name', 'expiration_date', 'cvv']
        extra_kwargs = {
            'card_number': {'required': True},
            'cardholder_name': {'required': True},
            'expiration_date': {'required': True},
            'cvv': {'required': True},
        }

    def validate_card_number(self, value):
        if not re.match(r'^\d{4}\s\d{4}\s\d{4}\s\d{4}$', value):
            raise serializers.ValidationError(
                "Некорректный формат номера карты"
            )
        return value

    def validate(self, attrs):
        print(attrs)
        client = self.context.get('client')
        self.save_card = self.context.get('request').query_params.get('save')
        if self.save_card and PaymentRequisites.objects.filter(
            card_number=attrs.get('card_number'), client=client
        ).exists():
            self.save_card = False
        return attrs

    def create(self, validated_data, **kwargs):
        return PaymentRequisites.objects.create(**validated_data)


class PaymentRequisitesUpdateGetSerializer(serializers.ModelSerializer):
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Удаление поля 'cvv' из представления данных
        data.pop('cvv', None)
        return data
