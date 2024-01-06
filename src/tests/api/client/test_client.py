# from django.test import TestCase, Client
# from bronfood.core.client.models import Client as ClientModel


# class ClientURLTests(TestCase):
#     @classmethod
#     def setUp(self):
#         # Создаем неавторизованый клиент
#         self.guest_client = Client()

#     def test_client_signup_location(self):
#         """Проверка доступности адреса /client/signup/."""
#         response = self.guest_client.get('/client/signup/')
#         self.assertEqual(response.status_code, 200)


# from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient


client = APIClient()

# factory = APIRequestFactory()
# request = factory.post('/client/signup/',
#                        data={'password': 'password',
#                              'phone': '700000000',
#                              'fullname': 'New client'},
#                        format='json'
#                        )
# request = client.post('/client/signup/',
#                        data={'password': 'password',
#                              'phone': '700000000',
#                              'fullname': 'New client'},
#                        format='json'
#                        )
# self.assertEqual(response.status_code, 200)
# print()

from django.contrib.auth.hashers import check_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bronfood.core.client.models import Client


class ClientApiTests(APITestCase):
    def test_create_client(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('client:signup')
        data = {'password': 'password',
                'phone': '7000000000',
                'fullname': 'New client'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Client.objects.get().phone, data['phone'])
        self.assertEqual(Client.objects.get().fullname, data['fullname'])
        client_hash_password = Client.objects.get().password
        is_password_correct = check_password(data['password'],
                                             client_hash_password)
        self.assertTrue(is_password_correct)
