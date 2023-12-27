from rest_framework import serializers
from bronfood.core.payment_requisites.models import PaymentRequisites


class PaymentRequisitesCreateSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = PaymentRequisites
        fields = ['card_number', 'cardholder_name', 'expiration_data', 'cvv']

    def create(self, validated_data, **kwargs):
        print(self.initial_data)
        print(validated_data)
        print(kwargs)
        return PaymentRequisites.objects.create(**validated_data)
