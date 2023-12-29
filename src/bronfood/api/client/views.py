from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

from bronfood.api.constants import ERR_MESSAGE
from bronfood.api.views import BaseAPIView
from bronfood.api.client.serializers import (
    ClientSerializer,
    ClientLoginSerializer,
    ClientUpdateSerializer,
    ClientPasswordResetSerializer,
    ClientResponseSerializer,
    ConfirmationSerializer,
    ClientRequestPasswordResetSerializer
)
from bronfood.core.client.models import Client, UserAccount


class ClientProfileView(BaseAPIView):
    permission_classes = (IsAuthenticated,)
    """
    Получение данных о клиенте, направившем get запрос.
    Обновление сведений о клиенте, направившим запрос patch.
    Требует авторизации.
    """

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Profile',
        responses={
            status.HTTP_200_OK: ClientResponseSerializer(),
            status.HTTP_400_BAD_REQUEST: ERR_MESSAGE[400],
            status.HTTP_401_UNAUTHORIZED: ERR_MESSAGE[401]
        }
    )
    def get(self, request):
        # Используется для предоставленя сведений о клиенте в профиле.
        serializer = ClientResponseSerializer(
            data={'phone': self.current_client.phone,
                  'fullname': self.current_client.fullname}
        )
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Update profile',
        request_body=ClientUpdateSerializer(),
        responses={
            status.HTTP_200_OK: ClientResponseSerializer(),
            status.HTTP_400_BAD_REQUEST: ERR_MESSAGE[400],
        }
    )
    # NOTE: в фигме для изменения данных в профиле клиента предусмотрено
    # подтверждение с СМС, что выглядит избыточным.
    # Изменения вносятся авторизованным клиентом.
    # Изменяются поля (пароль и Имя Фамилия).
    # Нет никакой ниобходимости подтверждать номер телефона.
    def patch(self, request):
        # Используется для обновления сведений о профиле клиента.
        serializer = ClientUpdateSerializer(self.current_client,
                                            data=request.data,
                                            partial=True)
        if serializer.is_valid():
            serializer.save()
            # Повторная аутентификация пользователя после сохранения изменений
            login(request, self.current_client)
            responce_serializer = ClientResponseSerializer(
                data={'phone': self.current_client.phone,
                      'fullname': self.current_client.fullname}
            )
            responce_serializer.is_valid()
            return Response(responce_serializer.data,
                            status=status.HTTP_200_OK)
        return Response(ERR_MESSAGE[400], status=status.HTTP_400_BAD_REQUEST)


class ClientLoginView(BaseAPIView):
    serializer_class = ClientLoginSerializer

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Login',
        request_body=ClientLoginSerializer(),
        responses={
            status.HTTP_200_OK: ClientResponseSerializer(),
            status.HTTP_400_BAD_REQUEST: ERR_MESSAGE[400],
            status.HTTP_401_UNAUTHORIZED: ERR_MESSAGE[401],
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone')
        password = serializer.validated_data.get('password')

        user = authenticate(request=request,
                            phone=phone,
                            password=password)

        if not user:
            return Response(ERR_MESSAGE[401],
                            status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        response_serializer = ClientResponseSerializer(data={'phone': phone})
        response_serializer.is_valid(raise_exception=True)
        return Response(response_serializer)


class ClientLogoutView(BaseAPIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Logout',
        responses={
            status.HTTP_204_NO_CONTENT: '',
        }
    )
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientPasswordResetView(BaseAPIView):
    """
    Восстановление пароля клиента на основе телефона и нового пароля.
    """
    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Request reset password',
        # request_body=ClientSerializer(),
        # TODO тут падает свагер
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_404_NOT_FOUND: ERR_MESSAGE[404],
        }
    )
    def get(self, request):
        # pass
        serializer = ClientRequestPasswordResetSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone')
        client = get_object_or_404(Client, phone=phone)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Reset password',
        request_body=ClientPasswordResetSerializer(),
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_404_NOT_FOUND: ERR_MESSAGE[404],
        }
    )
    def post(self, request):
        serializer = ClientPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone')
        new_password = serializer.validated_data.get('new_password')
        client = get_object_or_404(Client, phone=phone)
        client.set_password(new_password)
        client.save(update_fields=['password'])
        return Response(status=status.HTTP_200_OK)


class ClientRegistrationView(BaseAPIView):
    """
    Создание и авторизация нового клиента.
    """
    serializer_class = ClientSerializer

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Registration',
        request_body=ClientSerializer(),
        responses={
            status.HTTP_200_OK: ClientResponseSerializer(),
            status.HTTP_400_BAD_REQUEST: ERR_MESSAGE[400],
        }
    )
    def post(self, request):
        # Создание клиента
        client_serializer = self.serializer_class(data=request.data)
        client_serializer.is_valid(raise_exception=True)
        # Создание клиента
        client_serializer.save()
        # Авторизация клиента
        phone = client_serializer.validated_data.get('phone')
        password = client_serializer.validated_data.get('password')

        user = authenticate(
            request=request,
            phone=phone,
            password=password,
        )
        login(request, user)
        # Используем сериализатор для возврата данных
        fullname = client_serializer.validated_data.get('fullname')
        response_serializer = ClientResponseSerializer(
            data={'phone': phone,
                  'fullname': fullname})
        response_serializer.is_valid(raise_exception=True)
        return Response(response_serializer.validated_data,
                        status=status.HTTP_200_OK)


class ClientConfirmationView(BaseAPIView):
    permission_classes = (IsAuthenticated,)
    """
    Подтверждение клиента.
    """
    serializer_class = ConfirmationSerializer
    VALID_CODE = "0000"

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Client confirmation',
        request_body=ConfirmationSerializer(),
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_400_BAD_REQUEST: ERR_MESSAGE[400],
            status.HTTP_401_UNAUTHORIZED: ERR_MESSAGE[401],
        }
    )
    def post(self, request):
        confirmation_serializer = self.serializer_class(data=request.data)
        confirmation_serializer.is_valid(raise_exception=True)
        confirmation_code = confirmation_serializer.validated_data['confirmation_code']
        # Получаем авторизованного пользователя из запроса

        try:
            ...
            # какая-то функция из клиента проверяет confirmation_code
        except Exception as e:
            # какой-то Exception - выбрасывает клиент по валидации смс,
            # если оно неверпное, нужно обработать и сделать Validation error
            raise ValidationError('Invalid confirmation code')
        else:
            self.current_client.status = UserAccount.Status.CONFIRMED
            self.current_client.save(update_fields=['status', ])

        return Response(status=status.HTTP_200_OK)
