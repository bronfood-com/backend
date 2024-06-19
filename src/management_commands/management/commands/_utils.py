import logging
import os
import random
import shutil

from rest_framework.exceptions import ValidationError

from bronfood.core.restaurants.models import Meal
from ._variables import (
    COUNT_MOCK_DATA, MEAL_NAMES, MEAL_DESCRIPTIONS, PATH_TO_MEALS_IMAGE_DIR,
    PATH_TO_MEDIA_PICS_FOLDER
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def random_string(names):
    '''Возвращает случайную строку из списка.'''
    return random.choice(names)


def random_phone_number():
    "Возвращает случайный номер телефона."
    return f'7{random.randint(1000000000, 9999999999)}'


def get_random_image(folder_path, target_folder):
    """Получаем путь для папки из которой нужно выбрать случайное изображение
    и путь до папки куда нужно его копировать.
    Если папки в которую нужно копировать не существует, создаём её.
    Возвращаем путь скопированного изображения.
    """
    images = os.listdir(folder_path)
    random_image = random.choice(images)
    random_image_path = os.path.join(folder_path, random_image)
    try:
        os.makedirs(target_folder)
    except FileExistsError:
        pass
    return shutil.copy(random_image_path, target_folder)


def create_meals(count=COUNT_MOCK_DATA):
    """Создаёт несколько моковых блюд в базе"""
    count_validate(count)

    meals = [
        Meal(
            name=random_string(MEAL_NAMES),
            description=random_string(MEAL_DESCRIPTIONS),
            waitingTime=random.randint(1, 120),
            price=random.randint(10, 500),
            photo=get_random_image(
                PATH_TO_MEALS_IMAGE_DIR, PATH_TO_MEDIA_PICS_FOLDER
            ),
            type=random.choice(Meal.MEAL_TYPES)[0]
        )
        for i in range(count)
    ]
    meals_in_bd = Meal.objects.bulk_create(meals)
    logging.info(f'Создано {str(count)} блюд.')
    return meals_in_bd


def count_validate(count):
    """Проверяет входящее значение."""
    if count < 1 or count > 100:
        raise ValidationError(
            'Можно создать от 1 до 100 объектов за один раз.'
        )
