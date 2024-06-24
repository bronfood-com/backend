import random
import string
from django.core.exceptions import ObjectDoesNotExist


def generate_order_id():
    '''Функция генерации уникального индентификатора заказа'''
    while True:
        id = ''.join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(6)
        )
        try:
            from bronfood.core.restaurants.models import Order
            Order.objects.get(id=id)
        except ObjectDoesNotExist:
            return id


def create_order(*args, **kwargs):
    '''Функция создания нового заказа'''
    order_id = generate_order_id()
    kwargs.setdefault('id', order_id)
    from bronfood.core.restaurants.models import Order
    order = Order(*args, **kwargs)
    order.save()
    return order
