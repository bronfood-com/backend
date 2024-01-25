from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
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
    # ClientChangePasswordConfirmationSerializer,
    # ClientChangePasswordRequestSerializer, ClientChangePasswordSerializer,
    ClientLoginSerializer, ClientResponseSerializer,
    # ClientSerializer,
    ClientUpdateSerializer, ConfirmationSerializer,
    ClientDataToProfileSerializer,
    ClientRequestRegistrationSerializer,
    # ClientUpdatePasswordSerializer
)
from bronfood.api.constants import HTTP_STATUS_MSG
from bronfood.api.views import BaseAPIView
from bronfood.core.client.models import Client, UserAccount
from bronfood.core.useraccount.models import UserAccountTempData

from bronfood.api.client.utils import error_data


class ClientRequestRegistrationView(BaseAPIView):
    """
    Создание объекта клиента с неподтвержденным статусом.
    Формирование и отравка кода подтверждения клиенту на телефон.
    """
    serializer_class = ClientRequestRegistrationSerializer

    def post(self, request):
        client_serializer = self.serializer_class(data=request.data)
        client_serializer.is_valid(raise_exception=True)
        # Создание неподтвержденного клиента
        client_serializer.save()
        client = client_serializer.instance

        # Создание объекта UserAccountTempData
        temp_data_obj = UserAccountTempData.objects.create(
            temp_data_code=UserAccountTempData.get_unique_data_code(),
            user=client
        )
        temp_data_obj.save()

        # TODO: создание СМС с нужной причиной в объекте клинта
        # и отправка на телефон
        response_data = {
            'temp_data_code': temp_data_obj.temp_data_code,
        }
        return Response(
            data=response_data,
            status=status.HTTP_201_CREATED)


class ClientRegistrationView(BaseAPIView):
    """
    Аутентификация клиента при получении валидного кода подтверждения.
    """
    CONFIRMATION_CODE = '0000'

    def post(self, request):
        temp_data_code = request.data.get('temp_data_code')
        confimation_code = request.data.get('confimation_code')

        if confimation_code != self.CONFIRMATION_CODE:
            return Response(
                data=error_data(HTTP_STATUS_MSG[400]),
                status=status.HTTP_400_BAD_REQUEST
            )

        temp_data = get_object_or_404(UserAccountTempData,
                                      temp_data_code=temp_data_code)
        client = temp_data.user

        # TODO: добавить проверку кода подтверждения у клиента.
        # если есть активный код подтверждения у клиента
        # если причина создания кода подтверждения - регистрация
        # то осуществляю аутентификацию и перевод клиента в активный статус

        client.status = UserAccount.Status.CONFIRMED
        client.save(update_fields=['status', ])
        temp_data.delete()
        token, created = Token.objects.get_or_create(user=client)
        # Формирование ответа
        response_data = {
            'phone': client.phone,
            'fullname': client.fullname,
            'auth_token': token.key
        }
        return Response(response_data,
                        status=status.HTTP_200_OK)


class ClientChangePasswordRequestView(BaseAPIView):
    """
    Клиент делает запрос на смену пароля.
    Отправляет телефон.
    Выполняются проверки:
    - валидности формата телефона.
    - наличия клиента с таким телефоном.
    Вовращает уникальный код, связанный с объектом клиента.
    """
    # TODO: проверить как у владельца осуществляется восстановление пароля.

    def post(self, request):
        client_phone = request.data.get('phone')
        # проверить в сериализаторе, что верный формат телефона
        client = Client.objects.filter(phone=client_phone).first()
        if not client:
            # сообщить, что пользователя с таким телефоном отсутствует
            return Response(
                data=error_data(HTTP_STATUS_MSG[404]),
                status=status.HTTP_404_NOT_FOUND
            )
        # Создание объекта UserAccountTempData
        temp_data_obj = UserAccountTempData.objects.create(
            temp_data_code=UserAccountTempData.get_unique_data_code(),
            user=client
        )
        temp_data_obj.save()
        response_data = {
            'status': 'success',
            'data': {
                'temp_data_code': temp_data_obj.temp_data_code
            }
        }
        return Response(
            data=response_data,
            status=status.HTTP_200_OK)


class ClientChangePasswordConfirmationView(BaseAPIView):
    """
    Клиент вводит новый пароль.
    Выполняются проверки:
    - валидности формата пароля.
    - пароль и повторный пароль совпадают.
    Предложенный пароль временно сохраняется в бд.
    Формируется, сохраняется в бд и направляется клиенту код подтверждения.
    Вовращает id клиента.
    """
    # TODO: проверить как у владельца осуществляется восстановление пароля.

    def post(self, request):
        temp_data_code = request.data.get('temp_data_code')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')
        if new_password != new_password_confirm:
            return Response(
                data=error_data(HTTP_STATUS_MSG[400]),
                status=status.HTTP_400_BAD_REQUEST
            )
        # получение объекта клиента из кода
        temp_data = get_object_or_404(UserAccountTempData,
                                      temp_data_code=temp_data_code)
        client = temp_data.user
        temp_data.delete()

        # TODO: создание СМС с нужной причиной в объекте клинта
        # и отправка на телефон

        # Создание объекта UserAccountTempData
        temp_data_obj = UserAccountTempData.objects.create(
            temp_data_code=UserAccountTempData.get_unique_data_code(),
            user=client,
            new_password=new_password
        )
        temp_data_obj.save()

        response_data = {
            'status': 'success',
            'data': {
                'temp_data_code': temp_data_obj.temp_data_code
            }
        }
        return Response(
            data=response_data,
            status=status.HTTP_200_OK)


class ClientChangePasswordCompleteView(BaseAPIView):
    """
    Восстановление пароля клиента.
    Изменяется пароль на новый.
    Клиент получает токен.
    """
    CONFIRMATION_CODE = '0000'

    def patch(self, request):
        temp_data_code = request.data.get('temp_data_code')
        confimation_code = request.data.get('confimation_code')

        temp_data = get_object_or_404(UserAccountTempData,
                                      temp_data_code=temp_data_code)
        client = temp_data.user

        if confimation_code != self.CONFIRMATION_CODE:
            return Response(
                data=error_data(HTTP_STATUS_MSG[400]),
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {'new_password': temp_data.new_password}

        serializer = ClientUpdateSerializer(client,
                                            data=data,
                                            partial=True)
        serializer.is_valid()
        serializer.save()

        temp_data.delete()
        token, created = Token.objects.get_or_create(user=client)

        response_data = {
            'status': 'success',
            'data': {
                'phone': client.phone,
                'fullname': client.fullname,
                'auth_token': token.key
            }
        }
        return Response(response_data,
                        status=status.HTTP_200_OK)


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
        confirmation_code = serializer.validated_data.pop(
            'confirmation_code', None)
        # TODO Добавить проверку кода подтверждения
        serializer.save()
        responce_serializer = ClientResponseSerializer(
            data={'phone': self.current_client.phone,
                  'fullname': self.current_client.fullname}
        )
        return Response(responce_serializer.initial_data,
                        status=status.HTTP_200_OK)


class ClientDataToProfileView(BaseAPIView):
    """
    Временная заглушка до решения о том, 
    как будут доставляться данные в эндпоинт 'profile'
    для изменения данных и получения подтверждение клиента.
    Реализовыавать тут изменения данных без полученя подтвержденя, не имеет смысла.
    
    Создает и сохраняет СМС в БД для подтверждения.
    Направляет СМС код клиенту на телефон через оператора.
    Получает и возвращает данные для изменения профиля клиента.
    Требует авторизации.
    """
    
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Data_to_update profile',
        request_body=ClientDataToProfileSerializer(),
        responses={
            status.HTTP_200_OK: ClientDataToProfileSerializer(),
            status.HTTP_400_BAD_REQUEST: HTTP_STATUS_MSG[400],
        }
    )    
    def post(self, request):
        serializer = ClientDataToProfileSerializer(self.current_client,
                                                  data=request.data,
                                                  partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(request.data,
                        status=status.HTTP_200_OK)
  

# class ClientChangePasswordCompleteView(BaseAPIView):
#     """
#     Восстановление пароля клиента.
#     Изменяется пароль на новый и получает токен.
#     """
#     @swagger_auto_schema(
#         tags=['client'],
#         operation_summary='Сhange password',
#         request_body=ClientChangePasswordSerializer(),
#         responses={
#             status.HTTP_200_OK: ClientResponseSerializer(),
#             status.HTTP_404_NOT_FOUND: HTTP_STATUS_MSG[404],
#         }
#     )
#     def patch(self, request):
#         pass
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


class ClientDataToRegistrationView(BaseAPIView):
    """
    Временная заглушка до решения о том, 
    как будут доставляться данные в эндпоинт 'signup'
    для создания и подтверждение клиента. 
    Создавать тут клиента, не имеющего подтвержденя телефона, не имеет смысла.
    
    Создает и сохраняет СМС в БД для подтверждения номера клиента.
    Направляет СМС код клиенту на телефон через оператора.
    Получает и возвращает данные для создания клиента.
    """
    serializer_class = ClientRequestRegistrationSerializer

    @swagger_auto_schema(
        tags=['client'],
        operation_summary='Get data and make SMS request',
        request_body=ClientRequestRegistrationSerializer(),
        responses={
            status.HTTP_201_CREATED: ClientRequestRegistrationSerializer(),
            status.HTTP_400_BAD_REQUEST: HTTP_STATUS_MSG[400],
        }
    )
    def post(self, request):
        client_serializer = self.serializer_class(data=request.data)
        client_serializer.is_valid(raise_exception=True)
        response_data = {
            'phone': request.data['phone'],
            'fullname': request.data['fullname'],
            'password':  request.data['password']
        }
        return Response(response_data,
                        status=status.HTTP_200_OK)


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
        additional_data = {'fullname': token.user.fullname, 'phone': token.user.phone}
        response_data.update(additional_data)
        response_serializer = ClientLoginSerializer(data=response_data)
        return Response(
            data=response_serializer.initial_data, status=status.HTTP_200_OK
        )

# class ClientRegistrationView(BaseAPIView):
#     """
#     Создание объекта клиента с неподтвержденным статусом.
#     Формирование и отравка кода подтверждения клиенту на телефон.
#     """
#     serializer_class = ClientSerializer

#     @swagger_auto_schema(
#         tags=['client'],
#         operation_summary='Signup',
#         request_body=ClientSerializer(),
#         responses={
#             status.HTTP_201_CREATED: ClientLoginSerializer(),
#             status.HTTP_400_BAD_REQUEST: HTTP_STATUS_MSG[400],
#         }
#     )
#     def post(self, request):
#         client_serializer = self.serializer_class(data=request.data)
#         client_serializer.is_valid(raise_exception=True)
#         # Получение кода подтверждения из сериалайзера
#         confirmation_code = client_serializer.validated_data.pop('confirmation_code', None)
#         # TODO Добавить проверку кода подтверждения
#         # Создание клиента
#         client_serializer.save()
#         # Аутентификация пользователя
#         authenticated_user = authenticate(
#             request=request,
#             phone=client_serializer.validated_data.get('phone'),
#             password=client_serializer.validated_data['password']
#         )
#         if authenticated_user is not None:
#             # Выдача токена
#             token, created = Token.objects.get_or_create(user=authenticated_user)
#             # Формирование ответа
#             response_data = {
#                 'phone': authenticated_user.phone,
#                 'fullname': authenticated_user.fullname,
#                 'auth_token': token.key
#             }
#             response_serializer = ClientLoginSerializer(data=response_data)
#             return Response(response_serializer.initial_data,
#                             status=status.HTTP_201_CREATED)
#         else:
#             return Response({'error': 'Failed to authenticate user'}, status=status.HTTP_401_UNAUTHORIZED)