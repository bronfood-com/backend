from django.test import TestCase

from bronfood.core.client.models import Client
from bronfood.core.restaurants.models import (
    Coordinates, Meal, Menu, Restaurant, Tag, Feature, Favorites
)


class TaskModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tag = Tag.objects.create(name='test')
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
            rating=9.9,
            workingTime='10:00-22:00',
            type='cafe'
        )
        cls.restaurant.meals.set([cls.meal_1])

    def test_title_label(self):
        """verbose_name поля title совпадает с ожидаемым."""
        tags = TaskModelTest.tag
        meals = TaskModelTest.meal_1
        restaurants = TaskModelTest.restaurant
        # Получаем из свойства класса Task значение verbose_name для title
        verboset = tags._meta.get_field('name').verbose_name
        self.assertEqual(verboset, 'Название')
        verbosed = meals._meta.get_field('name').verbose_name
        self.assertEqual(verbosed, 'Название блюда')
        verboser = restaurants._meta.get_field('address').verbose_name
        self.assertEqual(verboser, 'Адрес')


class RestaurantModelTest(TestCase):
    '''Тест модели Restaurant'''
    def setUp(self):
        self.coordinates = Coordinates.objects.create(
            latitude=11.111111,
            longitude=22.222222
        )
        self.meal = Meal.objects.create(
            id='1',
            name='doner',
            description='test doner',
            photo='test',
            price=100,
            type='food',
            waitingTime=99
        )
        self.restaurant = Restaurant.objects.create(
            id=1,
            name='Turckish',
            photo='test',
            address='Palace',
            coordinates=self.coordinates,
            rating=9.9,
            workingTime='10:00-22:00',
            type='cafe'
        )
        self.restaurant.meals.set([self.meal])

    def test_fields(self):
        restaurant = self.restaurant
        self.assertEqual(restaurant.id, 1)
        self.assertEqual(restaurant.name, 'Turckish')
        self.assertEqual(restaurant.photo, 'test')
        self.assertEqual(restaurant.address, 'Palace')
        self.assertEqual(restaurant.coordinates, self.coordinates)
        self.assertEqual(restaurant.rating, 9.9)
        self.assertEqual(restaurant.workingTime, '10:00-22:00')
        self.assertEqual(restaurant.type, 'cafe')
        self.assertQuerysetEqual(
            restaurant.meals.all(), [self.meal], transform=lambda x: x
        )


class MealModelTest(TestCase):
    '''Тест модели Meal'''
    def setUp(self):
        self.feature = Feature.objects.create(name='test')
        self.meal = Meal.objects.create(
            id=1,
            name='doner',
            description='test doner',
            photo='test',
            price=100,
            type='food',
            waitingTime=99
        )
        self.meal.features.set([self.feature])

    def test_fields(self):
        meal = self.meal
        self.assertEqual(meal.id, 1)
        self.assertEqual(meal.name, 'doner')
        self.assertEqual(meal.description, 'test doner')
        self.assertEqual(meal.photo, 'test')
        self.assertEqual(meal.price, 100)
        self.assertEqual(meal.type, 'food')
        self.assertEqual(meal.waitingTime, 99)
        self.assertQuerysetEqual(
            meal.features.all(), [self.feature], transform=lambda x: x
        )


class FavoritesModelTest(TestCase):
    '''Тест модели Favorites'''
    def setUp(self):
        self.coordinates = Coordinates.objects.create(
            latitude=11.1111,
            longitude=22.2222
        )
        self.restaurant = Restaurant.objects.create(
            id=1,
            name='Turckish',
            photo='test',
            address='Palace',
            coordinates=self.coordinates,
            rating=9.9,
            workingTime='10:00-22:00',
            type='cafe'
        )
        self.user = Client.objects.create(
            username='testuser',
            password='12345',
            phone='1234567890'
        )
        self.favorite = Favorites.objects.create(
            user=self.user, restaurant=self.restaurant
        )

    def test_fields(self):
        favorite = self.favorite
        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.restaurant, self.restaurant)
        self.assertEqual(str(favorite), f"{self.user} - {self.restaurant}")
