from django.db import models
from bronfood.core.client.models import Client
from bronfood.core.restaurants.models import Restaurant
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    '''Отзывы о заказе в ресторане'''

    client = models.ForeignKey(
        Client,
        related_name='reviews',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Клиент'
    )
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Ресторан'
    )
    comment = models.TextField(
        null=True,
        blank=True
    )
    rating = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name='Оценка'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __repr__(self) -> str:
        return (
            f'Отзыв {self.pk} клиента {self.client} '
            f'по ресторану {self.restaurant.name}'
        )
