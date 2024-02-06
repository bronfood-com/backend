from django.urls import path
from bronfood.api.payment_requisites.views import (
    PaymentRequisitesCreateView,
    PaymentRequisitesUpdateGetView
)

app_name = 'requisites'
urlpatterns = [
    path(
        'users/bank-card/',
        PaymentRequisitesCreateView.as_view(),
        name='payment_requisites_list'
    ),
    path(
        'users/bank-card/<int:card_id>/',
        PaymentRequisitesUpdateGetView.as_view(),
        name='payment_requisites_detail'
    ),
]
