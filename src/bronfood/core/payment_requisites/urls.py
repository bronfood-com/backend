from django.urls import path

from bronfood.api.payment_requisites.views import PaymentRequisitesView

app_name = 'requisites'
urlpatterns = [
    path('users/<int:user_id>/bank-card', PaymentRequisitesView.as_view(), name='payment-requisites')
]
