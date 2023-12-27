from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from bronfood.core.client.models import Client


class PaymentRequisites(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    # restaurant_owner = ...
    card_number = models.CharField(max_length=16)
    cardholder_name = models.CharField(max_length=255)
    expiration_data = models.CharField()
    cvv = models.IntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(999)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
