from django.test import TestCase
from bronfood.core.restaurant_admin.models import RestaurantAdmin
from bronfood.core.restaurants.models import Coordinates, Meal, Restaurant
from bronfood.core.useraccount.models import UserAccount


class RestaurantAdminCRUDTest(TestCase):
    def setUp(self):
        self.user = UserAccount.objects.create_user(
            phone='1234567890',
            username='testuser',
            password='testpassword'
        )
        self.coordinates = Coordinates.objects.create(latitude=50.4501, longitude=30.5234)
        self.meal = Meal.objects.create(name='Test Meal', price=10.0, waitingTime=30.0)
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            photo='http://example.com/photo.jpg',
            address='123 Test St',
            coordinates=self.coordinates,
            rating=4.5,
            workingTime='10:00 - 22:00',
            type='cafe'
        )
        self.restaurant.meals.add(self.meal)
        self.admin = RestaurantAdmin.objects.create(
            login='adminlogin',
            password='adminpassword',
            restaurant_owner=self.user,
            restaurant=self.restaurant
        )

    def test_create_restaurant_admin(self):
        '''Тест создания администратора ресторана'''
        self.assertEqual(RestaurantAdmin.objects.count(), 1)
        self.assertEqual(self.admin.login, 'adminlogin')
        self.assertEqual(self.admin.password, 'adminpassword')
        self.assertEqual(self.admin.restaurant_owner, self.user)
        self.assertEqual(self.admin.restaurant, self.restaurant)

    def test_update_restaurant_admin(self):
        '''Тест обновления администратора ресторана'''
        self.admin.login = 'newlogin'
        self.admin.save()
        self.assertEqual(self.admin.login, 'newlogin')

    def test_read_restaurant_admin(self):
        '''Тест чтения администратора ресторана'''
        admin = RestaurantAdmin.objects.get(login='adminlogin')
        self.assertEqual(admin, self.admin)

    def test_delete_restaurant_admin(self):
        '''Тест удаления администратора ресторана'''
        self.admin.delete()
        self.assertEqual(RestaurantAdmin.objects.count(), 0)
