from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bronfood.core.client.models import Client
from bronfood.api.payment_requisites.serializers import PaymentRequisitesCreateSerializer
from rest_framework.serializers import ModelSerializer
from typing import TypeVar


PaymentRequisites = TypeVar('PaymentRequisites', bound=ModelSerializer)


class PaymentRequisitesView(APIView):
    # После реализвации кастомных пермишенов изменить на IsAuthenticatedRestaurantOwner
    # или IsAuthenticatedClient
    permission_classes = [IsAuthenticated,]

    @staticmethod
    def check_exist_card(client: Client, validation_data: PaymentRequisites):
        card = client.bank_card.filter(
            cvv=validation_data.validated_data.get('cvv'),
            card_number=validation_data.validated_data.get('card_number'),
            cardholder_name=validation_data.validated_data.get('cardholder_name')
        )[0]
        return card

    def post(self, request, user_id, format=None):
        client = get_object_or_404(Client, id=user_id)
        serializer = PaymentRequisitesCreateSerializer(data=request.data)
        data_valid = serializer.is_valid()
        if not data_valid:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        card = self.check_exist_card(client, serializer)
        if card:
            return Response(
                {"карта с такими данными уже существует": serializer.data},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.query_params.get('save'):
            serializer.save(client=client)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_200_OK)
