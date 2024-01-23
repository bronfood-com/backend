from typing import TypeVar

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from bronfood.api.payment_requisites.serializers import (
    PaymentRequisitesCreateSerializer, PaymentRequisitesUpdateGetSerializer)
from bronfood.core.client.models import Client
from bronfood.core.payment_requisites.models import PaymentRequisites

PaymentRequisitesSerializer = TypeVar(
    'PaymentRequisitesSerializer', bound=ModelSerializer
)


class UserNotOwnCardAPIException(APIException):
    status_code = 400

    def __init__(self, detail=None, code=None):
        if detail is not None:
            self.detail = detail
        if code is not None:
            self.code = code
        super().__init__()


class PaymentRequisitesCreateView(APIView):
    @classmethod
    def check_exist_card(
        cls,
        client: Client,
        validation_data: PaymentRequisitesSerializer
    ) -> PaymentRequisites:
        card = client.bank_card.filter(
            cvv=validation_data.validated_data.get('cvv'),
            card_number=validation_data.validated_data.get('card_number'),
            cardholder_name=validation_data.validated_data.get(
                'cardholder_name'
            )
        )
        return card

    def post(self, request, user_id, format=None) -> Response:
        '''Сохранение данных карты для конкретного пользователя.'''
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
                {'data': serializer.data,
                 'text_error': 'Данная карта уже принадлеждит пользователю.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.query_params.get('save'):
            serializer.save(client=client)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentRequisitesUpdateGetView(APIView):
    def put(self, request, user_id, card_id) -> Response:
        client: Client = get_object_or_404(Client, id=user_id)
        card: PaymentRequisites = get_object_or_404(
            PaymentRequisites, id=card_id)
        if not PaymentRequisites.objects.filter(
                client=client).select_related('client'):
            return Response(
                f'Пользователю {client.username} '
                f'не принадлежит карта {card.card_number}',
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = PaymentRequisitesUpdateGetSerializer(
            card,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, user_id, card_id):
        '''Получить данные карты для конкретного пользователя'''
        client = get_object_or_404(Client, id=user_id)
        card = get_object_or_404(PaymentRequisites, id=card_id)
        data = (
            PaymentRequisites.objects
            .filter(id=card.id, client=client)
            .select_related('client')
        )
        if not data:
            raise UserNotOwnCardAPIException(
                detail=(
                    f'Пользователю {client.username}'
                    f'не принадлежит карта с id-{card.id}'
                )
            )
        serializer = PaymentRequisitesUpdateGetSerializer(data[0])
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
