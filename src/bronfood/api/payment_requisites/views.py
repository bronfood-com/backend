from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bronfood.core.client.models import Client
from bronfood.core.payment_requisites.models import PaymentRequisites
from bronfood.api.payment_requisites.serializers import (
    PaymentRequisitesUpdateSerializer,
    PaymentRequisitesCreateSerializer
)
from rest_framework.serializers import ModelSerializer
from typing import TypeVar, Callable


PaymentRequisitesSerializer = TypeVar('PaymentRequisitesSerializer', bound=ModelSerializer)


class BasePaymentRequisites:
    def get_obj_with_id(self, obj_id: int, model: Callable):
        return get_object_or_404(model, id=obj_id)


class PaymentRequisitesCreateView(BasePaymentRequisites, APIView):
    # После реализвации кастомных пермишенов изменить на IsAuthenticatedRestaurantOwner
    # или IsAuthenticatedClient
    permission_classes = [IsAuthenticated,]

    @staticmethod
    def check_exist_card(
        client: Client,
        validation_data: PaymentRequisitesSerializer
    ) -> PaymentRequisites:
        card = client.bank_card.filter(
            cvv=validation_data.validated_data.get('cvv'),
            card_number=validation_data.validated_data.get('card_number'),
            cardholder_name=validation_data.validated_data.get('cardholder_name')
        )[0]
        return card

    def get_obj_with_id(self, obj_id, model):
        return get_object_or_404(model, id=obj_id)

    def post(self, request, user_id, format=None) -> Response:
        '''Сохранение данных карты для конкретного пользователя.'''
        client = self.get_obj_with_id(user_id, Client)
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


class PaymentRequisitesUpdateView(BasePaymentRequisites, APIView):
    def put(self, request, user_id, card_id) -> Response:
        client: Client = self.get_obj_with_id(user_id, Client)
        card: PaymentRequisites = get_object_or_404(
            PaymentRequisites, id=card_id)
        if not PaymentRequisites.objects.filter(client=client).select_related('client'):
            return Response(
                f"Пользователю {client.username} не принадлежит карта {card.card_number}",
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = PaymentRequisitesUpdateSerializer(
            card,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, user_id, card_id):
        '''Получить данные карты для конкретного пользователя'''
        client = self.get_obj_with_id(user_id, Client)
        data = (
            PaymentRequisites.objects
            .filter(id=card_id, client=client)
            .select_related('client')
        )
        if not data:
            return Response(
                f"Пользователю {client.username} не принадлежит карта под id-{card_id}",
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'card_number': data[0].card_number,
                'cardholder_name': data[0].cardholder_name,
                'cvv': data[0].cvv,
                'expiration_data': data[0].expiration_data
            },
            status=status.HTTP_200_OK
        )
