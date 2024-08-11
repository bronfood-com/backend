import os
from django.conf import settings
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from urllib.parse import urljoin

from bronfood.core.restaurants.models import Meal, Feature, Choice

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

IMAGE_PATH = '/src/management_commands/images/meals/'


class Command(BaseCommand):
    help = 'Создаёт моковые блюда.'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                self.create_meals()
                logging.info('Создано 4 моковых блюда')
        except Exception as e:
            logging.error(e)
            self.stdout.write(self.style.ERROR('Ошибка при создании моковых блюд'))

    def create_meals(self):
        meals_data = [
            {
                'name': 'Куриный донер',
                'description': 'Лаваш, курица, соленый огурец, помидор, капуста, лук, морковь, зелень.',
                'photo': IMAGE_PATH + 'meal1.png',
                'price': 1350,
                'type': 'food',
                'waitingTime': 10,
                'features': [
                    {
                        'name': 'Размер',
                        'choices': [
                            {'name': 'Маленький', 'price': 1050},
                            {'name': 'Средний', 'price': 1350, 'default': True},
                            {'name': 'Большой', 'price': 1650},
                        ],
                    },
                    {
                        'name': 'Соусы',
                        'choices': [
                            {'name': 'Кетчуп', 'price': 100, 'default': True},
                            {'name': 'Чесночный', 'price': 200},
                            {'name': 'Сырный', 'price': 300},
                        ],
                    },
                    {
                        'name': 'Овощи',
                        'choices': [
                            {'name': 'Томаты', 'price': 100, 'default': True},
                            {'name': 'Огурцы', 'price': 200},
                            {'name': 'Оливки', 'price': 300},
                            {'name': 'Маринованные огурцы', 'price': 400},
                            {'name': 'Зелень', 'price': 500},
                        ],
                    },
                ],
            },
            {
                'name': 'Говяжий донер',
                'description': 'Говядина',
                'photo': 'meal1.png',
                'price': 1350,
                'type': 'food',
                'waitingTime': 10,
                'features': [],
            },
            {
                'name': 'Американо',
                'description': 'Кофе',
                'photo': 'drink1.png',
                'price': 200,
                'type': 'drink',
                'waitingTime': 5,
                'features': [],
            },
            {
                'name': 'Пуддинг',
                'description': 'Пуддинг',
                'photo': 'dessert1.png',
                'price': 350,
                'type': 'dessert',
                'waitingTime': 5,
                'features': [],
            },
        ]
        for meal_data in meals_data:
            image_basename = os.path.basename(meal_data['photo'])
            image_url = urljoin(settings.MEDIA_URL, 'pics/' + image_basename)

            meal = Meal.objects.create(
                name=meal_data['name'],
                description=meal_data['description'],
                photo=image_url,
                price=meal_data['price'],
                type=meal_data['type'],
                waitingTime=meal_data['waitingTime'],
            )
            for feature_data in meal_data['features']:
                feature = Feature.objects.create(name=feature_data['name'], meal=meal)
                for choice_data in feature_data['choices']:
                    Choice.objects.create(
                        name=choice_data['name'],
                        price=choice_data.get('price', 0),
                        default=choice_data.get('default', False),
                        feature=feature
                    )
