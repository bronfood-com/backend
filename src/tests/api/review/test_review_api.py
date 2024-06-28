from django.contrib.auth.hashers import check_password
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from bronfood.api.client.serializers import ClientRequestRegistrationSerializer
from bronfood.core.client.models import Client
from bronfood.core.useraccount.models import UserAccount, UserAccountTempData
from bronfood.core.restaurants.models import (
    Coordinates, Meal, Menu, Restaurant
)
from bronfood.core.review.models import Review


class ReviewApiTests(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Клиент с токеном и подтверждением
        cls.data_authorized_client = {
            'password': 'password',
            'phone': '70000000002',
            'fullname': 'Client in DB'}
        cls.user = Client.objects.create(**cls.data_authorized_client)
        cls.user.status = UserAccount.Status.CONFIRMED
        cls.token = Token.objects.create(user=cls.user)

    # Ресторан
        cls.place = Coordinates.objects.create(
            latitude=11.111111,
            longitude=22.222222
        )
        cls.meal_1 = Meal.objects.create(
            id='1',
            name='doner',
            description='best doner',
            photo='test',
            price=100,
            type='food',
            waitingTime=99
        )
        menu = Menu.objects.create(
            category='fastfood'
        )
        menu.meals.set([cls.meal_1])
        cls.restaurant = Restaurant.objects.create(
            id=1,
            name='Turckish',
            photo='test',
            address='Palace',
            coordinates=cls.place,
            rating=3,
            workingTime='10:00-22:00',
            type='cafe'
        )
        cls.restaurant.meals.set([cls.meal_1])

    # Отзыв
        review_data = {
            'client': cls.user,
            'restaurant': cls.restaurant,
            'comment': 'Очень вкусно',
            'rating': 5
        }

        cls.review = Review.objects.create(**review_data)

    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest = APIClient()

        # Создаем авторизованый клиент
        self.authorized_client = APIClient()
        self.authorized_client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token}')

        # Данные для создания клиента при его регистрации
        self.registration_data = {
            'password': 'password',
            'phone': '70000000001',
            'fullname': 'Registered client'
        }

        self.confirmation_data = {'confirmation_code': '0000'}

    def test_get_rating(self):
        """
        Тест получения рейтинга ресторана.
        """
        url = reverse('review:reviews-get', kwargs={'restaurant_id': 1})
        response = self.authorized_client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'status': 'success',
            'data': {
                'restaurant_name': self.restaurant.name,
                'restaurant_rating': '3.0',
                'review_count': 1,
                'reviews': [
                    {
                        'comment': 'Очень вкусно',
                        'rating': 5,
                        'created_at': response.data['data']['reviews'][0]['created_at'],
                        'client_name': self.data_authorized_client['fullname']
                    }
                ]
            }
        }

        self.assertEqual(response.data,
                         expected_data,
                         'Response data error')

    def test_create_rating(self):
        """
        Тест создания отзыва ресторану.
        """
        url = reverse(
            'review:review-create',
            kwargs={'restaurant_id': 1}
        )
        data = {
            'rating': '4',
            'comment': 'Ни чо так'
        }
        response = self.authorized_client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'status': 'success',
            'data': None
        }
        self.assertEqual(response.data,
                         expected_data,
                         'Response data error')

        expected_count = 2
        self.assertEqual(Review.objects.count(),
                         expected_count,
                         'Review creation error')

        restaurant = Restaurant.objects.first()
        expected_rating = 3.5000
        self.assertEqual(
            restaurant.rating,
            expected_rating,
            'Rating restaurant creation error')
