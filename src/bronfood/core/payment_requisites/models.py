from django.core.validators import RegexValidator
from django.db import models

from bronfood.core.client.models import Client


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
        max_length=19,
        validators=[
            RegexValidator(
                regex=r'^\d{4}\s\d{4}\s\d{4}\s\d{4}$',
                code='invalid_card_number',
            )
        ],
        unique=True
    )
    cardholder_name = models.CharField(
        max_length=255,
        validators=[RegexValidator(regex=r'^[a-zA-Z]+\s[a-zA-Z]+$')]
    )
    expiration_date = models.CharField(max_length=255, validators=[
        RegexValidator(
            regex=r'^\d{2}/\d{2}$'
        )
    ])
    cvv = models.CharField(max_length=255, validators=[
        RegexValidator(regex=r'^\d{3}$')
    ])

    def __str__(self) -> str:
        return (f'Владелец карты {self.cardholder_name}, '
                f'номер карты {self.card_number}')
