from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from bronfood.core.client.models import Client
from django.db.models import UniqueConstraint
from django.core.validators import MinLengthValidator, MaxLengthValidator


class PaymentRequisites(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='bank_card'
    )
    # restaurant_owner = ...
    card_number = models.CharField(
        validators=[
            MinLengthValidator(16), MaxLengthValidator(16)
        ]
    )
    cardholder_name = models.CharField(max_length=255)
    expiration_data = models.CharField()
    cvv = models.IntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(999)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (f'Владелец карты {self.cardholder_name}, '
                f'номер карты {self.card_number}')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['card_number', 'cvv', 'cardholder_name'],
                name='unique_card_number_cvv_cardholder_name'
            ),
        ]
