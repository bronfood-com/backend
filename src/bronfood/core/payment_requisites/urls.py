from django.urls import path

from bronfood.api.payment_requisites.views import (
    PaymentRequisitesCreateView,
    PaymentRequisitesUpdateView
)


app_name = 'requisites'
urlpatterns = [
    path(
        'users/<int:user_id>/bank-card',
        PaymentRequisitesCreateView.as_view(),
        name='payment-requisites'
    ),
    path(
        'users/<int:user_id>/bank-card/<int:card_id>',
        PaymentRequisitesUpdateView.as_view(),
        name='payment-requisites'
    ),
]
