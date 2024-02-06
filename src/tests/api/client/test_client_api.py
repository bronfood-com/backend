# import unittest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bronfood.core.client.models import Client
from bronfood.core.useraccount.models import UserAccount, UserAccountTempData
from django.contrib.auth.hashers import check_password
from bronfood.api.client.serializers import ClientRequestRegistrationSerializer
from rest_framework.authtoken.models import Token


class ClientApiTests(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        

        # Данные для авторизованного и активированного клиента 
        cls.data_authorized_client = {
            'password': 'password',
            'phone': '7000000002',
            'fullname': 'Client in DB'}
        serializer = ClientRequestRegistrationSerializer(
            data=cls.data_authorized_client)
        serializer.is_valid()
        cls.user = serializer.save()
        # подтвержденный статус
        cls.user.status = UserAccount.Status.CONFIRMED
        # Создадим токен для авторизации
        cls.token = Token.objects.create(user=cls.user)


        # Данные для неавторизованного и активированного клиента 
        cls.data_to_signin = {'password': 'password',
                              'phone': '7000000000',
                              'fullname': 'New client'}
        serializer = ClientRequestRegistrationSerializer(
            data=cls.data_to_signin)
        serializer.is_valid()
        cls.client_to_signin = serializer.save()
        cls.client_to_signin.status = UserAccount.Status.CONFIRMED
    
        # Данные неавторизованного и неактивированного клиента 
        cls.data_inactive = {'password': 'superpassword',
                             'phone': '7000000005',
                             'fullname': 'Client to activate'}
        serializer = ClientRequestRegistrationSerializer(
            data=cls.data_inactive)
        serializer.is_valid()
        cls.client_inactive = serializer.save()
        cls.temp_obj_inctive = (
            UserAccountTempData.objects.create(
                user = cls.client_inactive
            )
        )
        cls.activation_data = {
            'temp_data_code': cls.temp_obj_inctive.temp_data_code,
            'confirmation_code': '0000'
        }


    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest = APIClient()
        
        # Создаем авторизованый клиент
        self.authorized_client = APIClient()
        self.authorized_client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token}')

        self.client_data = {'password': 'password',
                            'phone': '7000000000',
                            'fullname': 'New client'}
        # self.client = Client.objects.create(**self.client_data)
        # self.authorized_client.force_login(self.client)

        # Данные для создания клиента при его регистрации
        self.registration_data = {
            'password': 'password',
            'phone': '7000000001',
            'fullname': 'Registered client'
        }

        self.confirmation_data = {'confirmation_code': '0000'}

    def test_request_to_signup(self):
        """
        Ensure we can create a new client object.
        """
        url = reverse('client:request_to_signup')
        count_clients_before = Client.objects.count()
        response = self.guest.post(
            url, self.registration_data, format='json'
        )

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED,
                         'Not correct status code response')

        self.assertEqual(Client.objects.count(),
                         count_clients_before + 1,
                         'Client not created')
        
        registered_client = Client.objects.get(
            phone=self.registration_data['phone'])

        self.assertEqual(
            registered_client.fullname,
            self.registration_data['fullname'],
            'Client fullname error')

        is_password_correct = check_password(self.registration_data['password'],
                                             registered_client.password)
        self.assertTrue(is_password_correct,
                        'Password hash error')
        
        self.assertEqual(
            registered_client.role, 'CLIENT',
            'User role is not Client')
        
        client_temp_data_code = (
            UserAccountTempData.objects.filter(
                user=registered_client.id).first().temp_data_code
        )
        expected_data = {
            'status': 'success',
            'data': {
                'temp_data_code': client_temp_data_code
            }
        }
        self.assertEqual(response.data,
                         expected_data,
                         'Response data format error')


    # TODO: до начала теста нужно создать временный объект в базе данных к клиенту
    def test_signup(self):
        """
        Ensure we can activate client and send him token.
        """
        url = reverse('client:signup')
        status_client_before = self.client_inactive.status
        response = self.guest.post(
            url, self.activation_data, format='json'
        )
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED,
                         'Wrong data')
        client_id = self.client_inactive.pk
        status_client_after = Client.objects.get(id=client_id).status
        self.assertNotEqual(
            status_client_before,
            status_client_after,
            'Client status does not changed'
        )
        self.assertEqual(status_client_after,
                         UserAccount.Status.CONFIRMED,
                         'Client status does not cofirmed')
        
        token = Token.objects.filter(user=self.client_inactive).first()
        
        expected_data = {
            'status': 'success',
            'data': {
                'phone': self.client_inactive.phone,
                'fullname': self.client_inactive.fullname,
                'auth_token': token.key
            }
        }
        self.assertEqual(response.data,
                         expected_data,
                         'Response data format error')


    def test_get_profile(self):
        """
        Ensure only authorized_client get correct profile.
        """
        url = reverse('client:profile')
        response = self.authorized_client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'status': 'success',
            'data': {
                "phone": self.data_authorized_client['phone'],
                "fullname": self.data_authorized_client['fullname']
            }
        }
        self.assertEqual(response.data,
                         expected_data,
                         'Response data error')
        
        # неавторизованное обращение
        response = self.guest.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    # @unittest.skip(
    #     'Для прохождения теста нужно отключить валидацию на основе '
    #     'регулярных выражений в сериализаторе ClientUpdateSerializer'
    # )
    def test_profile_update_request(self):
        """
        Ensure authorized client can update password,
        fullname and phone.
        """
        data = {
            'password': 'superpuper',
            'password_confirm': 'superpuper',
            'fullname': 'XXX',
            'phone': '7121212000'
        }
        url = reverse('client:profile_update_request')

        response = self.authorized_client.post(
            url, data=data, format='json'
        )
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         'Wrong status code response')
        # добавить проверку создания корректного временного объекта
        client_temp_data = (
            UserAccountTempData.objects.filter(
                user=self.user.id).first()
        )
        self.assertEqual(client_temp_data.fullname, data['fullname'])
        self.assertEqual(client_temp_data.phone, data['phone'])
        # TODO добавить проверку client_temp_data.password после
        # того как будет настроено сохранение хэша пароля во временные данные
        
        temp_data_code = client_temp_data.temp_data_code
        expected_data = {
            'status': 'success',
            'data': {
                'temp_data_code': temp_data_code
            }
        }
        self.assertEqual(response.data,
                         expected_data,
                         'Response data format error')

        # # получение хэша пароля клиента
        # updated_client_hash_password = Client.objects.get(
        #     fullname='updated client').password
        # # сравнение хэшей паролей
        # is_password_updated = check_password(updated_data['new_password'],
        #                                      updated_client_hash_password)
        # self.assertTrue(is_password_updated)

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

    def test_signout(self):
        """
        Ensure signout client.
        """
        url = reverse('client:signout')
        client = Client.objects.get(phone=self.data_authorized_client['phone'])

        # Проверяем, что токен существует перед выходом (signout)
        is_token_before_signout = Token.objects.filter(
            user=client).exists()
        self.assertTrue(is_token_before_signout,
                        "Token should exist before signout")

        response = self.authorized_client.post(
            url, format='json')

        # Проверяем успешность выхода (HTTP 204)
        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT)

        # Проверяем, что токен отсутствует после выхода (signout)
        is_token_after_signout = Token.objects.filter(
            user=client).exists()
        self.assertFalse(is_token_after_signout,
                         "Token should not exist after signout")


    def test_signin(self):
        """
        Ensure signin client.
        """
        url = reverse('signin')

        # обращение клиента за авторизацией
        response = self.guest.post(
            url,
            data={'phone': self.data_to_signin['phone'],
                  'password': self.data_to_signin['password']},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        client = Client.objects.get(phone=self.data_to_signin['phone'])
        token = Token.objects.filter(user=client).first()
        expected_data = {
            'status': 'success',
            'data': {
                'auth_token': token.key,
                'fullname': self.data_to_signin['fullname'],
                'phone': self.data_to_signin['phone'],
                'role': 'CLIENT'
            }
        }
        self.assertEqual(response.data,
                         expected_data,
                         'Response data error')
        
        # некорректное обращение
        response = self.guest.post(
            url,
            data={'phone': self.data_to_signin['phone'],
                  'password': 'wrong_password'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_change_password_request(self):
        """
        Ensure unauthorized client can send request to change password.
        """
        url = reverse('client:change_password_request')
        data = {'phone': self.data_to_signin['phone']}
        response = self.guest.post(url,
                                   data=data,
                                   format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         'Wrong status code response')

        client_temp_data_code = (
            UserAccountTempData.objects.filter(
                user=self.client_to_signin.id).first().temp_data_code
        )
        expected_data = {
            'status': 'success',
            'data': {
                'temp_data_code': client_temp_data_code
            }
        }
        self.assertEqual(response.data,
                         expected_data,
                         'Response data format error')


        wrong_data = {'phone': '7111111111'}
        response = self.guest.post(url,
                                   data=wrong_data,
                                   format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            'Wrong phone can start change_password_request'
        )


    def test_change_password_confirmation(self):
        """
        Ensure unauthorized client send confirmation code
        and can authorize to change password.
        """
        temp_data_code = (
            UserAccountTempData.objects.create(
                user = self.client_to_signin,
            )
        ).temp_data_code

        url = reverse('client:change_password_confirmation')

        data = {
            'temp_data_code': temp_data_code,
            'password': 'super200',
            'password_confirm': 'super200'
        }
        response = self.guest.post(url,
                                   data=data,
                                   format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

        client_temp_data_code = (
            UserAccountTempData.objects.filter(
                user=self.client_to_signin.id).first().temp_data_code
        )
        expected_data = {
            'status': 'success',
            'data': {
                'temp_data_code': client_temp_data_code
            }
        }
        self.assertEqual(response.data,
                         expected_data,
                         'Response data format error')

    def test_change_password_complete(self):
        """
        Ensure unauthorized client can finalize change password procedure
        and set new password.
        """
        temp_data_code = (
            UserAccountTempData.objects.create(
                user = self.client_to_signin,
            )
        ).temp_data_code
        
        url = reverse('client:change_password_complete')

        data = {
            'temp_data_code': temp_data_code,
            'confirmation_code': '0000'
        }
        response = self.guest.patch(url,
                                    data=data,
                                    format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        
        expected_data = {
            'status': 'success',
            'data': {
                'message': 'Password updated'
            }
        }
        self.assertEqual(response.data,
                         expected_data,
                         'Response data format error')
