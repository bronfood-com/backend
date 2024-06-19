import logging
import random

from django.core.management.base import BaseCommand

from bronfood.core.restaurants.models import (
    Coordinates, Meal, Menu, Restaurant, Tag
)
from ._variables import (
    COUNT_MOCK_DATA, MENU_CATEGORIES, RESTAURANT_TAGS, RESTAURANT_NAMES,
    RESTAURANT_ADDRESSES, RESTAURANT_DESCRIPTIONS, BEGIN_TIMES, END_TIMES,
    PATH_TO_RESTAURANTS_IMAGE_DIR, PATH_TO_MEDIA_PICS_FOLDER
)
from ._utils import (
    random_string, get_random_image, create_meals, count_validate
)


def create_menu(meals, restaurants_count=COUNT_MOCK_DATA):
    """Создаёт несколько моковых меню в базе"""
    menu = [
        Menu(
            category=random_string(MENU_CATEGORIES)
        )
        for i in range(int(restaurants_count))
    ]
    menu_in_bd = Menu.objects.bulk_create(menu)
    for menu in menu_in_bd:
        menu.meals.add(*meals)
    logging.info(f'Создано {str(restaurants_count)} меню.')
    return menu_in_bd


def create_restaurants(count=COUNT_MOCK_DATA, meal_count=COUNT_MOCK_DATA):
    """Создаёт несколько моковых ресторанов в базе"""

    count_validate(count)

    tag, created = Tag.objects.get_or_create(name=random_string(RESTAURANT_TAGS))

    if meal_count > Meal.objects.all().count():
        meals = create_meals(meal_count)
    else:
        meals = Meal.objects.all()[:meal_count]

    menu = create_menu(meals, count)

    restaurants = [
        Restaurant(
            name=random_string(RESTAURANT_NAMES),
            photo=get_random_image(
                PATH_TO_RESTAURANTS_IMAGE_DIR, PATH_TO_MEDIA_PICS_FOLDER
            ),
            address=random_string(RESTAURANT_ADDRESSES),
            coordinates=Coordinates.objects.create(
                latitude=11.111111,
                longitude=22.222222
            ),
            rating=random.randint(50, 100),
            workingTime=f"{random_string(BEGIN_TIMES)} - {random_string(END_TIMES)}",
            type=random.choice(
                [choice[0] for choice in Restaurant.RESTAURANT_TYPES]
            ),
        )
        for i in range(count)
    ]
    restaurants_in_bd = Restaurant.objects.bulk_create(restaurants)
    for restaurant, menu_item in zip(restaurants_in_bd, menu):
        restaurant.meals.add(*menu_item.meals.all())
    logging.info(f'Создано {str(count)} ресторанов.')
    return restaurants_in_bd


class Command(BaseCommand):
    help = 'Создаёт моковых Ресторанов.'

    def handle(self, *args, **options):
        try:
            create_restaurants(options.get('count'), options.get('meal_count'))
        except Exception as e:
            return logging.error(e)

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=COUNT_MOCK_DATA,
            help='Добавляет заданное колличество ресторанов в базу.'
        )
        parser.add_argument(
            '--meal_count',
            type=int,
            default=COUNT_MOCK_DATA,
            help='Колличество блюд в меню для каждого ресторана.'
        )
