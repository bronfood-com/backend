from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bronfood.api.client.serializers import (
    ClientRequestRegistrationSerializer,
    TempDataCodeSerializer, TempDataSerializer, PhoneValidationSerializer)
from bronfood.api.client.utils import error_data, success_data
from bronfood.api.views import BaseAPIView
from bronfood.core.client.models import Client, UserAccount
from bronfood.core.useraccount.models import UserAccountTempData

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
                data=error_data('ValidationError'),
                status=status.HTTP_400_BAD_REQUEST
            )

        elif Client.objects.filter(phone=request.data['phone']).exists():
            return Response(
                data=error_data('phoneNumberIsAlreadyUsed'),
                status=status.HTTP_409_CONFLICT
            )

        # Создание неподтвержденного клиента
        client_serializer.save()
        client = client_serializer.instance

        # Создание объекта UserAccountTempData
        temp_data_obj = UserAccountTempData.objects.create_temp_data(
            user=client
        )

        # TODO: создание СМС с нужной причиной в объекте клиента
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
        temp_data_code = request.data.get('temp_data_code')
        confirmation_code = request.data.get('confirmation_code')
        temp_serializer = TempDataCodeSerializer(
            data={'temp_data_code': temp_data_code})

        temp_data = UserAccountTempData.get_object(temp_data_code)

        if not temp_serializer.is_valid() or not temp_data:
            return Response(
                data=error_data('ValidationError'),
                status=status.HTTP_400_BAD_REQUEST
            )

        if confirmation_code != CONFIRMATION_CODE:
            return Response(
                data=error_data('invalidConformationCode'),
                status=status.HTTP_404_NOT_FOUND
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
    Вовращает уникальный код, связанный с объектом клиента.
    """
    serializer_class = PhoneValidationSerializer

    def post(self, request):
        client_serializer = self.serializer_class(data=request.data)
        if not client_serializer.is_valid():
            return Response(
                data=error_data('ValidationError'),
                status=status.HTTP_400_BAD_REQUEST
            )

        client_phone = request.data.get('phone')
        # TODO проверить в сериализаторе, что верный формат телефона
        client = Client.objects.filter(phone=client_phone).first()

        if not client:
            return Response(
                data=error_data('UserWithThatPhoneNotFound'),
                status=status.HTTP_404_NOT_FOUND
            )

        temp_data_obj = UserAccountTempData.objects.create_temp_data(
            user=client
        )

        response_data = {'temp_data_code': temp_data_obj.temp_data_code}
        return Response(
            data=success_data(response_data),
            status=status.HTTP_200_OK
        )


class ClientChangePasswordConfirmationView(BaseAPIView):
    """
    Клиент вводит новый пароль.
    Выполняются проверки:
    - валидности формата пароля.
    - пароль и повторный пароль совпадают.
    Предложенный пароль временно сохраняется в бд.
    Формируется, сохраняется в бд и направляется клиенту код подтверждения.
    """

    serializer_class = TempDataSerializer

    def post(self, request):

        temp_data_obj = UserAccountTempData.get_object(
            request.data['temp_data_code']
        )

        data = request.data
        data['user'] = temp_data_obj.user.id
        temp_data_serializer = self.serializer_class(
            data=data
        )
        if not temp_data_serializer.is_valid() or not temp_data_obj:
            return Response(
                data=error_data('ValidationError'),
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создание временных данных
        temp_data_serializer.save()

        # # TODO: создание СМС с нужной причиной в объекте клинта
        # # и отправка на телефон

        response_data = {
            'temp_data_code': temp_data_serializer.instance.temp_data_code}
        return Response(
            data=success_data(response_data),
            status=status.HTTP_200_OK
        )


class ClientChangePasswordCompleteView(BaseAPIView):
    """
    Восстановление пароля клиента.
    Изменяется пароль на новый.
    """

    def patch(self, request):
        temp_data_code = request.data.get('temp_data_code')
        confirmation_code = request.data.get('confirmation_code')
        temp_serializer = TempDataCodeSerializer(
            data={'temp_data_code': temp_data_code})

        temp_data_obj = UserAccountTempData.get_object(temp_data_code)

        if not temp_serializer.is_valid() or not temp_data_obj:
            return Response(
                data=error_data('ValidationError'),
                status=status.HTTP_400_BAD_REQUEST
            )

        if confirmation_code != CONFIRMATION_CODE:
            return Response(
                data=error_data('invalidConformationCode'),
                status=status.HTTP_404_NOT_FOUND
            )

        client = temp_data_obj.user
        # Преобразуем объект temp_data в словарь с использованием сериализатора
        temp_data_serializer = TempDataSerializer(temp_data_obj)
        data = temp_data_serializer.data
        # обновляем данные клиента
        client.update_from_dict(data)
        return Response(success_data({'message': 'Password updated'}),
                        status=status.HTTP_200_OK)


class ClientProfileView(BaseAPIView):
    permission_classes = (IsAuthenticated,)
    """
    Получение данных о клиенте, направившем get запрос.
    Обновление сведений о клиенте, направившим запрос patch.
    Требует авторизации.
    """

    def get(self, request):
        response_data = {
            'fullname': self.current_client.fullname,
            'phone': self.current_client.phone,
            'role': self.current_client.role,
            'auth_token': self.current_client.auth_token.key,
        }
        return Response(success_data(response_data),
                        status=status.HTTP_200_OK)

    def patch(self, request):
        confirmation_code = request.data.get('confirmation_code')
        if confirmation_code != CONFIRMATION_CODE:
            return Response(
                data=error_data('invalidConformationCode'),
                status=status.HTTP_404_NOT_FOUND
            )

        temp_data_obj = UserAccountTempData.objects.filter(
            user=self.current_client.id).first()
        if not temp_data_obj:
            return Response(
                data=error_data('NoDataToUpdate'),
                status=status.HTTP_400_BAD_REQUEST
            )

        client = temp_data_obj.user
        # Преобразуем объект temp_data в словарь с использованием сериализатора
        temp_data_serializer = TempDataSerializer(temp_data_obj)
        data = temp_data_serializer.data
        # Обновляем данные клиента
        client.update_from_dict(data)

        response_data = {
            'fullname': client.fullname,
            'phone': client.phone,
            'role': client.role,
            'auth_token': client.auth_token.key
        }

        return Response(
            success_data(response_data),
            status=status.HTTP_200_OK)


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
                data=error_data('ValidationError'),
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создание временных данных
        temp_data_serializer.save()

        response_data = {
            'temp_data_code': temp_data_serializer.instance.temp_data_code
        }

        return Response(success_data(response_data),
                        status=status.HTTP_200_OK)
