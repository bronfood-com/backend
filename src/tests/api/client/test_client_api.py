# import unittest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bronfood.core.client.models import Client
from bronfood.core.useraccount.models import UserAccount
from django.contrib.auth.hashers import check_password
from bronfood.api.client.serializers import ClientSerializer


class ClientApiTests(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД
        client_data = {'password': 'password',
                       'phone': '7000000002',
                       'fullname': 'Base Client'}
        serializer = ClientSerializer(data=client_data)
        serializer.is_valid()
        serializer.save()

    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest = APIClient()

        # Создаем авторизованый клиент
        self.authorized_client = APIClient()
        self.client_data = {'password': 'password',
                            'phone': '7000000000',
                            'fullname': 'New client'}
        self.client = Client.objects.create(**self.client_data)
        self.authorized_client.force_login(self.client)

        # Данные для создания клиента при его регистрации
        self.registration_client_data = {
            'password': 'password',
            'phone': '7000000001',
            'fullname': 'Registered client'
        }

        self.confirmation_data = {'confirmation_code': '0000'}

    def test_create_client(self):
        """
        Ensure we can create a new client object.
        """
        url = reverse('client:signup')
        count_clients_before = Client.objects.count()
        response = self.guest.post(
            url, self.registration_client_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # количество клиентов увеличилось на один после выполнения регистрации
        self.assertEqual(
            Client.objects.count(),
            count_clients_before + 1
        )
        # получаю зарегистрированного клиента
        registered_client = Client.objects.get(
            phone=self.registration_client_data['phone']
        )

        self.assertEqual(
            registered_client.fullname,
            self.registration_client_data['fullname']
        )
        # Проверка верно ли установлен в бд хэш пароля клиента при создании
        registered_client_hash_password = registered_client.password
        is_password_correct = check_password(
            self.registration_client_data['password'],
            registered_client_hash_password)
        self.assertTrue(is_password_correct)
        # Проверяем, что после регистрации сессия установлена
        self.assertIn('_auth_user_id', self.guest.session)

    def test_get_profile(self):
        """
        Ensure only authorized_client get correct profile.
        """
        url = reverse('client:profile')
        # обращение авторизованного клиента
        response = self.authorized_client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'],
                         self.client_data['phone'])
        self.assertEqual(response.data['fullname'],
                         self.client_data['fullname'])
        # неавторизованное обращение
        response = self.guest.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # @unittest.skip(
    #     'Для прохождения теста нужно отключить валидацию на основе '
    #     'регулярных выражений в сериализаторе ClientUpdateSerializer'
    # )
    def test_update_profile(self):
        """
        Ensure client can update password and fullname.
        """
        url = reverse('client:profile')

        updated_data = {
            'new_password': 'updated password',
            'new_password_confirm': 'updated password',
            'fullname': 'updated client'
        }
        # обращение авторизованного клиента
        response = self.authorized_client.patch(
            url, data=updated_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # сущетвует ли клиент с обновленным именем
        self.assertTrue(Client.objects.get(fullname='updated client'))
        # получение хэша пароля клиента
        updated_client_hash_password = Client.objects.get(
            fullname='updated client').password
        # сравнение хэшей паролей
        is_password_updated = check_password(updated_data['new_password'],
                                             updated_client_hash_password)
        self.assertTrue(is_password_updated)

    def test_client_confirmation(self):
        """
        Ensure that confimation code change client status.
        """
        url = reverse('client:confirmation')
        # обращение авторизованного клиента
        client_status_before = self.client.status
        response = self.authorized_client.post(
            url, self.confirmation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # получаю клиента из бд для проверки изменения его статуса
        client_in_db = Client.objects.get(phone='7000000000')
        client_status_after = client_in_db.status
        self.assertNotEqual(client_status_before, client_status_after)
        self.assertEqual(client_status_after, UserAccount.Status.CONFIRMED)

    def test_client_logout(self):
        """
        Ensure loggout client.
        """
        url = reverse('client:signout')
        # Проверяем, что до разлогирования присутствует сессия
        self.assertIn('_auth_user_id', self.authorized_client.session)
        response = self.authorized_client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Проверяем, что после разлогирования сессия отсутствует
        self.assertNotIn('_auth_user_id', self.guest.session)

    def test_client_login(self):
        """
        Ensure loggin client.
        """
        url = reverse('client:signin')
        # Проверяем, что до регистрации отсутствует сессия
        self.assertNotIn('_auth_user_id', self.guest.session)
        # обращение клиента за авторизацией
        response = self.guest.post(url,
                                   data={'phone': '7000000002',
                                         'password': 'password'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что после логирования сессия установлена
        self.assertIn('_auth_user_id', self.guest.session)

    def test_change_password_request(self):
        """
        Ensure unauthorized client can send request to change password.
        """
        url = reverse('client:change_password_request')
        data = {'phone': '7000000002'}
        # обращение неавторизованного клиента
        response = self.guest.post(url,
                                   data=data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_change_password_change_password_confirmation(self):
        """
        Ensure unauthorized client send confirmation code
        and can authorize to change password.
        """
        url = reverse('client:change_password_confirmation')
        data = {"phone": "7000000002",
                "confirmation_code": "0000"}

        response = self.guest.post(url,
                                   data=data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # после отправки кода подтверждения установлена сессия
        self.assertIn('_auth_user_id', self.guest.session)

    def test_change_password_complete(self):
        """
        Ensure authorized client finalize change password procedure,
        set new password and loggin.
        """
        url = reverse('client:change_password_complete')
        request_data = {"new_password": "new_password",
                        "new_password_confirm": "new_password"}
        response_data = {"phone": "7000000000",
                         "fullname": "New client"}
        response = self.authorized_client.patch(url,
                                                data=request_data,
                                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)
        # после отправки кода подтверждения установлена сессия
        self.assertIn('_auth_user_id', self.authorized_client.session)
