from django.test import TestCase, Client as TestClient
from django.urls import reverse
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
        self.client = TestClient()
        self.user = Client.objects.create(
            username='testuser',
            password='12345',
            phone='1234567890'
        )
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
        response = self.client.get(
            reverse('user-favorites', kwargs={'user_id': self.user.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['id'], self.restaurant.id)


class DeleteUserFavoriteViewTest(TestCase):
    def setUp(self):
        self.client = TestClient()
        self.user = Client.objects.create(
            username='testuser',
            password='12345',
            phone='1234567890'
        )
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

    def test_delete_user_favorite(self):
        """
        Тест проверки удаления избранного ресторана пользователя
        """
        response = self.client.delete(
            reverse('delete-user-favorite',
                    kwargs={'user_id': self.user.id,
                            'restaurant_id': self.restaurant.id}))
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
        non_existent_restaurant_id = self.restaurant.id + 1
        response = self.client.delete(reverse(
            'delete-user-favorite',
            kwargs={'user_id': self.user.id,
                    'restaurant_id': non_existent_restaurant_id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['error_message'], 'Избранное не найдено')
