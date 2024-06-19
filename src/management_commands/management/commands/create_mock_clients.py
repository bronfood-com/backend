import logging
from django.core.management.base import BaseCommand
from rest_framework.exceptions import ValidationError
from ._utils import random_string, random_phone_number, count_validate
from ._variables import COUNT_MOCK_DATA, NAMES
from bronfood.core.client.models import Client


def create_clients(count=COUNT_MOCK_DATA, role=Client.Role.CLIENT):
    """Создаёт несколько моковых клиентов в базе"""

    if role not in Client.Role.values:
        raise ValidationError('Такой роли не существует.')
    count_validate(count)

    clients = [
        Client(
            role=role,
            username=random_string(NAMES),
            password='password',
            phone=random_phone_number(),
            fullname='{} {}'.format(random_string(NAMES), random_phone_number()),
            status=Client.Status.CONFIRMED
        )
        for i in range(count)
    ]
    clients_in_bd = Client.objects.bulk_create(clients)
    logging.info(f'Создано {str(count)} клиентов с ролью {role}')
    return clients_in_bd


class Command(BaseCommand):
    help = 'Создаёт моковых клиентов.'

    def handle(self, *args, **options):
        try:
            create_clients(options.get('count'), options.get('role'))
        except Exception as e:
            return logging.error(e)

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=COUNT_MOCK_DATA,
            help='Добавляет заданное колличество клиентов в базу.'
        )
        parser.add_argument(
            '--role',
            type=str,
            default=Client.Role.CLIENT,
            help='Указывает роль клиентов которых нужно добавить.'
        )
