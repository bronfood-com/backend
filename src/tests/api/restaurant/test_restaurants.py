from django.test import TestCase, Client as TestClient
from django.urls import reverse
from rest_framework.test import APIClient

from bronfood.core.restaurants.models import Restaurant, Favorites, Coordinates
from bronfood.core.client.models import Client


class UrlTests(TestCase):
    def test_get_restaurants(self):
        """
        Тест проверки получения статуса 200 при get запросе
        на адрес '/restaurant/'
        """
        guest_client = TestClient()
        response = guest_client.get("/api/restaurant/")
        self.assertEqual(response.status_code, 200)

    def test_get_menu(self):
        """
        Тест проверки получения статуса 200 при get запросе
        на адрес '/menus/'
        """
        guest_client = TestClient()
        response = guest_client.get("/api/menus/")
        self.assertEqual(response.status_code, 200)

    def test_get_meals(self):
        """
        Тест проверки получения статуса 200 при get запросе
        на адрес '/meals/'
        """
        guest_client = TestClient()
        response = guest_client.get("/api/meals/")
        self.assertEqual(response.status_code, 200)


class UserFavoritesViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Client.objects.create_user(
            username='testuser',
            password='12345',
            phone='1234567890'
        )
        self.client.force_authenticate(user=self.user)
        self.coordinates = Coordinates.objects.create(
            latitude=50.0000,
            longitude=30.0000
        )
        self.restaurant = Restaurant.objects.create(
            name='testrestaurant',
            rating=5,
            coordinates=self.coordinates
        )
        self.favorite = Favorites.objects.create(
            user=self.user,
            restaurant=self.restaurant
        )

    def test_get_user_favorites(self):
        """
        Тест проверки получения избранных ресторанов пользователя
        """
        response = self.client.get(reverse('favorite-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['id'], self.favorite.id)

    def test_create_user_favorite(self):
        """
        Тест проверки добавления ресторана в избранное
        """
        new_coordinates = Coordinates.objects.create(
            latitude=51.0000,
            longitude=31.0000
        )
        new_restaurant = Restaurant.objects.create(
            name='newrestaurant',
            rating=4,
            coordinates=new_coordinates
        )
        response = self.client.post(
            reverse('favorite-list'),
            {'user': self.user.id, 'restaurant': new_restaurant.id},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['data']['restaurant'], new_restaurant.id)

    def test_delete_user_favorite(self):
        """
        Тест проверки удаления избранного ресторана пользователя
        """
        response = self.client.delete(
            reverse('favorite-detail', kwargs={'pk': self.favorite.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'success')
        self.assertFalse(
            Favorites.objects.filter(
                user=self.user, restaurant=self.restaurant).exists()
        )

    def test_delete_nonexistent_favorite(self):
        """
        Тест проверки удаления несуществующего избранного ресторана пользователя
        """
        non_existent_favorite_id = self.favorite.id + 1
        response = self.client.delete(
            reverse('favorite-detail', kwargs={'pk': non_existent_favorite_id})
        )
        self.assertEqual(response.status_code, 404)
