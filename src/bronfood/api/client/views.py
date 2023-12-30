from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

from bronfood.api.constants import HTTP_STATUS_MSG
from bronfood.api.views import BaseAPIView
from bronfood.api.client.serializers import (
    ClientSerializer,
    ClientLoginSerializer,
    ClientUpdateSerializer,
    ClientResponseSerializer,
    ConfirmationSerializer,
    ClientChangePasswordSerializer,
    ClientChangePasswordRequestSerializer,
    ClientChangePasswordConfirmationSerializer,
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
            status.HTTP_400_BAD_REQUEST: HTTP_STATUS_MSG[400],
            status.HTTP_401_UNAUTHORIZED: HTTP_STATUS_MSG[401]
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
            status.HTTP_400_BAD_REQUEST: HTTP_STATUS_MSG[400],
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
        serializer.is_valid(raise_exception=True)
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


class ClientLoginView(BaseAPIView):
    serializer_class = ClientLoginSerializer

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Login',
        request_body=ClientLoginSerializer(),
        responses={
            status.HTTP_200_OK: ClientResponseSerializer(),
            status.HTTP_400_BAD_REQUEST: HTTP_STATUS_MSG[400],
            status.HTTP_401_UNAUTHORIZED: HTTP_STATUS_MSG[401],
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
            return Response(HTTP_STATUS_MSG[401],
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


class ClientChangePasswordRequestView(BaseAPIView):
    """
    Восстановление пароля клиента.
    ЭТАП 1. Предоставляется телефон.
    Оператору отправляется запрос на получение СМС.
    Полученный СМС сохраняется в БД.
    На телефон клиента отправляется СМС для подтверждения изменения пароля.
    """

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Request for change password',
        request_body=ClientChangePasswordRequestSerializer(),
        responses={
            status.HTTP_200_OK: ClientChangePasswordRequestSerializer(),
            status.HTTP_404_NOT_FOUND: HTTP_STATUS_MSG[404],
        }
    )
    def post(self, request):
        serializer = ClientChangePasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone')
        client = get_object_or_404(Client, phone=phone) # noqa
        # TODO запрос на получение клиентом СМС.
        # TODO сохранение в БД СМС для клиента.
        # TODO если выше прошло удачно возвращаем статус 200.
        return Response(serializer.validated_data,
                        status=status.HTTP_200_OK)


class ClientChangePasswordConfirmationView(BaseAPIView):
    """
    Восстановление пароля клиента.
    ЭТАП 2. Передается телефон и СМС.
    Полученный от клиента СМС сравниевает с тем, который в БД.
    Если ок, то клиент логинится.
    """
    # NOTE временная переменная до подключения получения СМС из БД
    VALID_CODE = "0000"

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Confirmation by sms for change password',
        request_body=ClientChangePasswordConfirmationSerializer(),
        responses={
            status.HTTP_200_OK: HTTP_STATUS_MSG[200],
            status.HTTP_400_BAD_REQUEST: HTTP_STATUS_MSG[400],
        }
    )
    def post(self, request):
        serializer = ClientChangePasswordConfirmationSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone')
        client = get_object_or_404(Client, phone=phone) # noqa
        confirmation_code = serializer.validated_data.get(  # noqa
            'confirmation_code'
        )
        try:
            # TODO получаем из БД СМС клиента
            # TODO проверяем что СМС из БД соответствует confirmation_code
            # NOTE временный код где проверяем, что confirmation_code
            # совпадает с VALID_CODE
            if confirmation_code != self.VALID_CODE:
                # Если код неверный, вызываем исключение ValidationError
                raise ValidationError('Invalid confirmation code')
                # Если код верный, логируем клиента
            login(request, client)
            return Response(status=status.HTTP_200_OK)

        except Exception as e:  # noqa
            # какой-то Exception - выбрасывает клиент по валидации смс,
            # если оно неверпное, нужно обработать и сделать Validation error
            raise ValidationError('Invalid confirmation code')


class ClientChangePasswordView(BaseAPIView):
    permission_classes = (IsAuthenticated,)
    """
    Восстановление пароля клиента.
    ЭТАП 3. Залогиненым изменяется пароль на новый.
    """

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Make change password',
        request_body=ClientChangePasswordSerializer(),
        responses={
            status.HTTP_200_OK: ClientResponseSerializer(),
            status.HTTP_404_NOT_FOUND: HTTP_STATUS_MSG[404],
        }
    )
    def patch(self, request):
        # Используется для обновления сведений о профиле клиента.
        serializer = ClientChangePasswordSerializer(self.current_client,
                                                    data=request.data)
        serializer.is_valid(raise_exception=True)
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


class ClientRegistrationView(BaseAPIView):
    """
    Создание и авторизация нового клиента.
    Отправка СМС для валидации телефона клиента.
    """
    serializer_class = ClientSerializer

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Registration',
        request_body=ClientSerializer(),
        responses={
            status.HTTP_200_OK: ClientResponseSerializer(),
            status.HTTP_400_BAD_REQUEST: HTTP_STATUS_MSG[400],
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
        # TODO запрос на получение клиентом СМС.
        # TODO сохранение в БД СМС для клиента.
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
            status.HTTP_400_BAD_REQUEST: HTTP_STATUS_MSG[400],
            status.HTTP_401_UNAUTHORIZED: HTTP_STATUS_MSG[401],
        }
    )
    def post(self, request):
        confirmation_serializer = self.serializer_class(data=request.data)
        confirmation_serializer.is_valid(raise_exception=True)
        confirmation_code = (
            confirmation_serializer.validated_data['confirmation_code']
        )

        try:
            # какая-то функция из клиента проверяет confirmation_code
            # NOTE временный код где проверяем, что confirmation_code
            # совпадает с VALID_CODE
            if confirmation_code != self.VALID_CODE:
                raise ValidationError('Invalid confirmation code')

        except Exception as e:  # noqa
            # какой-то Exception - выбрасывает клиент по валидации смс,
            # если оно неверпное, нужно обработать и сделать Validation error
            raise ValidationError('Invalid confirmation code')
        # BUG: ЭТОТ фрагмент не работает как нужно
        else:
            self.current_client.status = UserAccount.Status.CONFIRMED
            self.current_client.save(update_fields=['status', ])

        return Response(status=status.HTTP_200_OK)
