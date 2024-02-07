from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bronfood.api.client.serializers import (
    ClientUpdateSerializer,
    ClientRequestRegistrationSerializer,
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
        temp_data_obj = UserAccountTempData.objects.create_temp_data(user=client)

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
        confirmation_code = request.data.get('confirmation_code')
        error_message = None
        if not temp_data_code or not confirmation_code:
            error_message = 'Validation error'
        if confirmation_code != CONFIRMATION_CODE:
            error_message = 'Invalid_confirmation_code'

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
    Вовращает уникальный код, связанный с объектом клиента.
    """

    def post(self, request):
        client_phone = request.data.get('phone')
        #TODO проверить в сериализаторе, что верный формат телефона
        client = Client.objects.filter(phone=client_phone).first()
        
        if not client:
            return Response(
                data=error_data('Phone not found'),
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
            temp_data_code=request.data.get('temp_data_code'))
        if not temp_data_obj:
            return Response(
                data=error_data('Validation error'),
                status=status.HTTP_400_BAD_REQUEST
            )
        client_id = temp_data_obj.user.id


        data = request.data
        data['user'] = client_id
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

        # TODO: создание СМС с нужной причиной в объекте клинта
        # и отправка на телефон

        response_data = {'temp_data_code': temp_data_serializer.instance.temp_data_code}
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
        confirmation_code = request.data.get('confirmation_code')

        error_message = None
        if confirmation_code != CONFIRMATION_CODE:
            error_message = 'Validation error'

        temp_data_obj = UserAccountTempData.get_object(
            temp_data_code=request.data.get('temp_data_code'))

        if not temp_data_obj:
            error_message = 'Validation error'

        if error_message:
            return Response(
                data=error_data(error_message),
                status=status.HTTP_400_BAD_REQUEST
            )
        client = temp_data_obj.user
        # Преобразуем объект temp_data в словарь с использованием сериализатора
        temp_data_serializer = TempDataSerializer(temp_data_obj)
        
        data = temp_data_serializer.data
        data.pop('user')
        # Избегаем передачи атрибутов с None
        data = {key: value for key, value in data.items() if value is not None}
        
        # Обновляем данные у текущего клиента
        client.__dict__.update(data)
        client.save()

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
            'phone': self.current_client.phone,
            'fullname': self.current_client.fullname,
        }
        return Response(success_data(response_data),
                        status=status.HTTP_200_OK)


    def patch(self, request):
        confirmation_code = request.data.get('confirmation_code')

        error_message = None
        if confirmation_code != CONFIRMATION_CODE:
            error_message = 'Validation error'

        temp_data_obj = UserAccountTempData.objects.filter(
            user=self.current_client.id).first()

        if not temp_data_obj:
            error_message = 'Validation error'

        if error_message:
            return Response(
                data=error_data(error_message),
                status=status.HTTP_400_BAD_REQUEST
            )

        client = temp_data_obj.user
        # Преобразуем объект temp_data в словарь с использованием сериализатора
        temp_data_serializer = TempDataSerializer(temp_data_obj)
        data = temp_data_serializer.data

        data.pop('user')
        # Избегаем передачи атрибутов с None
        data = {key: value for key, value in data.items() if value is not None}
        
        # Обновляем данные у текущего клиента
        client.__dict__.update(data)
        client.save()
        return Response(success_data({'message': 'Profile updated successfully'}),
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
                data=error_data('Validation error'),
                status=status.HTTP_400_BAD_REQUEST
            )
        # Создание временных данных
        temp_data_serializer.save()

        response_data = {'temp_data_code': temp_data_serializer.instance.temp_data_code}

        return Response(success_data(response_data),
                        status=status.HTTP_200_OK)
    