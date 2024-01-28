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
    ClientUpdateSerializer,
    ConfirmationSerializer,
    ClientDataToProfileSerializer,
    ClientRequestRegistrationSerializer,
    # ClientUpdatePasswordSerializer,
    TempDataSerializer
)
from bronfood.api.constants import HTTP_STATUS_MSG
from bronfood.api.views import BaseAPIView
from bronfood.core.client.models import Client, UserAccount
from bronfood.core.useraccount.models import UserAccountTempData

from bronfood.api.client.utils import error_data, success_data


CONFIRMATION_CODE = '0000'

class ClientRequestRegistrationView(BaseAPIView):
    """
    Создание клиента без подтверждения статуса.
    Формирование и отравка кода подтверждения клиенту на телефон.
    """
    serializer_class = ClientRequestRegistrationSerializer

    def post(self, request):
        client_serializer = self.serializer_class(data=request.data)
        if not client_serializer.is_valid():
            return Response(
                data=error_data('Validation error'),
                status=status.HTTP_400_BAD_REQUEST
            )
        # Создание неподтвержденного клиента
        client_serializer.save()
        client = client_serializer.instance

        # Создание объекта UserAccountTempData
        temp_data_obj = UserAccountTempData.objects.create(user=client)
        temp_data_obj.save()

        # TODO: создание СМС с нужной причиной в объекте клинта
        # и отправка на телефон
        response_data = {'temp_data_code': temp_data_obj.temp_data_code}
        return Response(
            data=success_data(response_data),
            status=status.HTTP_201_CREATED)


class ClientRegistrationView(BaseAPIView):
    """
    Аутентификация клиента при получении валидного кода подтверждения.
    """

    def post(self, request):
        # TODO настроить обработку сериалайзером
        temp_data_code = request.data.get('temp_data_code')
        confimation_code = request.data.get('confimation_code')
        error_message = None
        if not temp_data_code or not confimation_code:
            error_message = 'Validation error'
        if confimation_code != CONFIRMATION_CODE:
            error_message = 'Invalid_confimation_code'

        temp_data = UserAccountTempData.get_object(temp_data_code)
        if not temp_data:
            error_message = 'Temp_data_error'

        if error_message:
            return Response(
                data=error_data(error_message),
                status=status.HTTP_400_BAD_REQUEST
            )

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
        return Response(
            data=success_data(response_data),
            status=status.HTTP_201_CREATED)


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


# class ClientChangePasswordCompleteView(BaseAPIView):
#     """
#     Восстановление пароля клиента.
#     Изменяется пароль на новый.
#     Клиент получает токен.
#     """

#     def patch(self, request):
#         temp_data_code = request.data.get('temp_data_code')
#         confimation_code = request.data.get('confimation_code')

#         temp_data = get_object_or_404(UserAccountTempData,
#                                       temp_data_code=temp_data_code)
#         client = temp_data.user

#         if confimation_code != CONFIRMATION_CODE:
#             return Response(
#                 data=error_data(HTTP_STATUS_MSG[400]),
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         data = {'new_password': temp_data.password}

#         serializer = ClientUpdateSerializer(client,
#                                             data=data,
#                                             partial=True)
#         serializer.is_valid()
#         serializer.save()

#         temp_data.delete()
#         token, created = Token.objects.get_or_create(user=client)

#         response_data = {
#             'status': 'success',
#             'data': {
#                 'phone': client.phone,
#                 'fullname': client.fullname,
#                 'auth_token': token.key
#             }
#         }
#         return Response(response_data,
#                         status=status.HTTP_200_OK)


class ClientProfileView(BaseAPIView):
    permission_classes = (IsAuthenticated,)
    """
    Получение данных о клиенте, направившем get запрос.
    Обновление сведений о клиенте, направившим запрос patch.
    Требует авторизации.
    """

    def get(self, request):
        response_data = {
            'phone': self.current_client.phone,
            'fullname': self.current_client.fullname,
        }
        return Response(success_data(response_data),
                        status=status.HTTP_200_OK)


    def patch(self, request):
        confimation_code = request.data.get('confimation_code')

        error_message = None
        if confimation_code != CONFIRMATION_CODE:
            error_message = 'Invalid_confimation_code'

        temp_data = UserAccountTempData.objects.filter(
            user=self.current_client.id).first()

        if not temp_data:
            error_message = 'Temp_data_error'

        if error_message:
            return Response(
                data=error_data(error_message),
                status=status.HTTP_400_BAD_REQUEST
            )

        # Преобразуем объект temp_data в словарь с использованием сериализатора
        temp_data_serializer = TempDataSerializer(temp_data)
        data = temp_data_serializer.data
        data.pop('user')

        # Обновляем данные у текущего клиента
        serializer = ClientUpdateSerializer(self.current_client,
                                            data=data,
                                            partial=True)
        if serializer.is_valid():
            serializer.save()
            temp_data.delete()
            return Response(success_data({'message': 'Profile updated successfully'}),
                            status=status.HTTP_200_OK)
        else:
            return Response(data=error_data('Validation error'),
                            status=status.HTTP_400_BAD_REQUEST)


class ClientRequestProfileUpdateView(BaseAPIView):
    permission_classes = (IsAuthenticated,)
    """
    Формирование данных для изменения профиля клиента.
    Отправка СМС с кодом подтверждения.
    Требует авторизации.
    """
    serializer_class = TempDataSerializer

    def post(self, request):
        data = request.data
        data['user'] = self.current_client.id
        temp_data_serializer = self.serializer_class(
            data=data
        )
        if not temp_data_serializer.is_valid():
            return Response(
                data=error_data('Validation error'),
                status=status.HTTP_400_BAD_REQUEST
            )
        # Создание временных данных
        temp_data_serializer.save()

        response_data = {
            'status': 'success',
            'data': {
                'temp_data_code': temp_data_serializer.instance.temp_data_code
            }
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
