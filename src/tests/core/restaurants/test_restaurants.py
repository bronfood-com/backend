from django.test import TestCase
from bronfood.core.restaurants.models import Restaurant, Menu, Tag, Dishes


class TaskModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовую запись в БД
        # и сохраняем созданную запись в качестве переменной класса
        cls.tag = Tag.objects.create(
            name='test'
        )
        cls.dishes = Dishes.objects.create(
            name='test',
            description='test',
            price=100,
            pic='test'
        )
        menu = Menu.objects.create(
            is_active=True
        )
        menu = Menu.objects.create(is_active=True)
        cls.restaurant = Restaurant.objects.create(
            title='test',
            adress='test',
            description='test',
            pic='test',
            from_work='test',
            to_work='test',
            type_of_restaurant='test',
            tags=cls.tag,
            is_canceled=False,
            rating=100
        )
        cls.restaurant.menu.set([menu])

    def test_title_label(self):
        """verbose_name поля title совпадает с ожидаемым."""
        tags = TaskModelTest.tag
        dishes = TaskModelTest.dishes
        restaurants = TaskModelTest.restaurant
        # Получаем из свойства класса Task значение verbose_name для title
        verboset = tags._meta.get_field('name').verbose_name
        self.assertEqual(verboset, 'Название')
        verbosed = dishes._meta.get_field('name').verbose_name
        self.assertEqual(verbosed, 'Название блюда')
        verboser = restaurants._meta.get_field('title').verbose_name
        self.assertEqual(verboser, 'Название ресторана')
