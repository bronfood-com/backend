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
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None) -> Response:
        '''Сохранение данных карты для конкретного пользователя.'''
        client = request.user
        serializer = PaymentRequisitesCreateSerializer(
            data=request.data, context={
                'client': client,
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        if not request.query_params.get('save'):
            return Response(serializer.data, status=status.HTTP_200_OK)
        if serializer.save_card:
            serializer.save(client=client)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {
                'data': serializer.data,
                'massege': 'Карту которую вы пытаетесь сохранить уже существует.'
            },
            status=status.HTTP_200_OK
        )


class PaymentRequisitesUpdateGetView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, card_id) -> Response:
        client: Client = request.user
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

    def get(self, request, card_id):
        '''Получить данные карты для конкретного пользователя'''
        client: Client = request.user
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
