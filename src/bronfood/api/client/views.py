from django.contrib.auth import authenticate
from djoser import utils
from djoser.conf import settings
from djoser.views import TokenCreateView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bronfood.api.client.serializers import (
    ClientChangePasswordSerializer,
    ClientLoginSerializer, ClientResponseSerializer, ClientSerializer,
    ClientUpdateSerializer, ConfirmationSerializer,
    ClientRequestSmsForSignupSerializer,
    ClientRequestSmsForProfileSerializer)
from bronfood.api.constants import HTTP_STATUS_MSG
from bronfood.api.views import BaseAPIView
from bronfood.core.client.models import UserAccount


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
        response_serializer = ClientResponseSerializer(
            data={'phone': self.current_client.phone,
                  'fullname': self.current_client.fullname}
        )
        return Response(response_serializer.initial_data,
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Update profile',
        request_body=ClientUpdateSerializer(),
        responses={
            status.HTTP_200_OK: ClientResponseSerializer(),
            status.HTTP_400_BAD_REQUEST: HTTP_STATUS_MSG[400],
        }
    )
    def patch(self, request):
        serializer = ClientUpdateSerializer(self.current_client,
                                            data=request.data,
                                            partial=True)
        serializer.is_valid(raise_exception=True)
        # получение кода подтверждения
        confirmation_code = serializer.validated_data.pop(  # noqa
            'confirmation_code', None)
        # TODO Добавить проверку кода подтверждения
        serializer.save()
        responce_serializer = ClientResponseSerializer(
            data={'phone': self.current_client.phone,
                  'fullname': self.current_client.fullname}
        )
        return Response(responce_serializer.initial_data,
                        status=status.HTTP_200_OK)


class ClientRequestSmsForProfileView(BaseAPIView):
    """
    Временная заглушка до решения о том,
    как будут доставляться данные в эндпоинт 'profile'
    для изменения данных и получения подтверждение клиента.
    Реализовыавать тут изменения данных
    без полученя подтвержденя, не имеет смысла.

    Создает и сохраняет СМС в БД для подтверждения.
    Направляет СМС код клиенту на телефон через оператора.
    Получает и возвращает данные для изменения профиля клиента.
    Требует авторизации.
    """

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='request_sms_for_profile',
        request_body=ClientRequestSmsForProfileSerializer(),
        responses={
            status.HTTP_200_OK: ClientRequestSmsForProfileSerializer(),
            status.HTTP_400_BAD_REQUEST: HTTP_STATUS_MSG[400],
        }
    )
    def post(self, request):
        serializer = ClientRequestSmsForProfileSerializer(
            self.current_client,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(request.data,
                        status=status.HTTP_200_OK)


class ClientChangePasswordView(BaseAPIView):
    """
    НЕ РЕАЛИЗОВАН
    Восстановление пароля клиента.
    Изменяется пароль на новый и получает токен.
    """
    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Сhange password',
        request_body=ClientChangePasswordSerializer(),
        responses={
            status.HTTP_200_OK: ClientResponseSerializer(),
            status.HTTP_404_NOT_FOUND: HTTP_STATUS_MSG[404],
        }
    )
    def patch(self, request):
        pass
#         # Используется для обновления сведений о профиле клиента.
#         serializer = ClientChangePasswordSerializer(self.current_client,
#                                                     data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # Повторная аутентификация пользователя после сохранения изменений
#         login(request, self.current_client)
#         responce_serializer = ClientResponseSerializer(
#             data={'phone': self.current_client.phone,
#                   'fullname': self.current_client.fullname}
#         )
#         responce_serializer.is_valid()
#         return Response(responce_serializer.data,
#                         status=status.HTTP_200_OK)


class ClientConfirmationView(BaseAPIView):
    """
    Подтверждение клиента.
    Есть сомнения в необходимости.
    Т.к. создание клиента без подтверждения не требуется.
    """
    permission_classes = (IsAuthenticated,)
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

        else:
            client = self.request.user
            client.status = UserAccount.Status.CONFIRMED
            client.save(update_fields=['status', ])
        return Response(status=status.HTTP_200_OK)


class ClientRequestSmsForSignupView(BaseAPIView):
    """
    Временная заглушка до решения о том,
    как будут доставляться данные в эндпоинт 'signup'
    для создания и подтверждение клиента.
    Создавать тут клиента, не имеющего подтвержденя телефона,
    не имеет смысла.

    Создает и сохраняет СМС в БД для подтверждения номера клиента.
    Направляет СМС код клиенту на телефон через оператора.
    Получает и возвращает данные для создания клиента.
    """
    serializer_class = ClientRequestSmsForSignupSerializer

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='request_sms_for_signup',
        request_body=ClientRequestSmsForSignupSerializer(),
        responses={
            status.HTTP_201_CREATED: ClientRequestSmsForSignupSerializer(),
            status.HTTP_400_BAD_REQUEST: HTTP_STATUS_MSG[400],
        }
    )
    def post(self, request):
        client_serializer = self.serializer_class(data=request.data)
        client_serializer.is_valid(raise_exception=True)
        response_data = {
            'phone': request.data['phone'],
            'fullname': request.data['fullname'],
            'password': request.data['password']
        }
        return Response(response_data,
                        status=status.HTTP_200_OK)


class ClientRegistrationView(BaseAPIView):
    """
    Создание и авторизация нового клиента.
    Отправка СМС для валидации телефона клиента.
    """
    serializer_class = ClientSerializer

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Signup',
        request_body=ClientSerializer(),
        responses={
            status.HTTP_201_CREATED: ClientLoginSerializer(),
            status.HTTP_400_BAD_REQUEST: HTTP_STATUS_MSG[400],
        }
    )
    def post(self, request):
        client_serializer = self.serializer_class(data=request.data)
        client_serializer.is_valid(raise_exception=True)
        # Получение кода подтверждения из сериалайзера
        confirmation_code = client_serializer.validated_data.pop(  # noqa
            'confirmation_code', None
        )
        # TODO Добавить проверку кода подтверждения
        # Создание клиента
        client_serializer.save()
        # Аутентификация пользователя
        authenticated_user = authenticate(
            request=request,
            phone=client_serializer.validated_data.get('phone'),
            password=client_serializer.validated_data['password']
        )
        if authenticated_user is not None:
            # Выдача токена
            token, created = Token.objects.get_or_create(
                user=authenticated_user)
            # Формирование ответа
            response_data = {
                'phone': authenticated_user.phone,
                'fullname': authenticated_user.fullname,
                'auth_token': token.key
            }
            response_serializer = ClientLoginSerializer(data=response_data)
            return Response(response_serializer.initial_data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to authenticate user'},
                            status=status.HTTP_401_UNAUTHORIZED)


class CustomTokenCreateView(TokenCreateView):
    """
    Custom token creation view with additional data.
    """
    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Login',
        request_body=ClientResponseSerializer(),
        responses={
            status.HTTP_201_CREATED: ClientLoginSerializer(),
            status.HTTP_400_BAD_REQUEST: HTTP_STATUS_MSG[400],
        }
    )
    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        response_data = token_serializer_class(token).data
        additional_data = {'fullname': token.user.fullname,
                           'phone': token.user.phone}
        response_data.update(additional_data)
        response_serializer = ClientLoginSerializer(data=response_data)
        return Response(
            data=response_serializer.initial_data, status=status.HTTP_200_OK
        )