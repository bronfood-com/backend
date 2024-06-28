from bronfood.core.useraccount.models import (
    UserAccount, UserAccountManager)
# from bronfood.core.restaurants.models import Restaurant
# from django.core.validators import MinValueValidator, MaxValueValidator
# from django.db import models


class ClientManager(UserAccountManager):

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(role=UserAccount.Role.CLIENT)
        return queryset


class Client(UserAccount):
    """ Модель Клиента"""

    def save(self, *args, **kwargs):
        self.role = UserAccount.Role.CLIENT
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.fullname

    class Meta:
        proxy = True
    objects = ClientManager()


# class Review(models.Model):
#     '''Отзывы о заказе в ресторане'''

#     client = models.ForeignKey(
#         Client,
#         related_name='review',
#         on_delete=models.SET_NULL,
#         null=True,
#         verbose_name='Клиент'
#     )
#     restaurant = models.ForeignKey(
#         Restaurant,
#         related_name='review',
#         on_delete=models.CASCADE,
#         verbose_name='Ресторан'
#     )
#     comment = models.TextField(
#         null=True,
#         blank=True
#     )
#     rating = models.DecimalField(
#         max_digits=1,
#         decimal_places=1,
#         validators=[
#             MinValueValidator(1),
#             MaxValueValidator(5)
#         ],
#         verbose_name='Оценка'
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     class Meta:
#         verbose_name = 'Отзыв'
#         verbose_name_plural = 'Отзывы'

#     def __repr__(self) -> str:
#         return (
#             f'Отзыв {self.pk} клиента {self.client} '
#             f'по ресторану {self.restaurant.name}'
#         )
