from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bronfood.core.client.models import Client
from bronfood.core.payment_requisites.serializers import \
    PaymentRequisitesCreateSerializer

class PaymentRequisitesView(APIView):
    # После реализвации кастомных пермишенов изменить на IsAuthenticatedRestaurantOwner
    # или IsAuthenticatedClient
    permission_classes = [IsAuthenticated,]

    def post(self, request, user_id, format=None):
        client = get_object_or_404(Client, id=user_id)
        serializer = PaymentRequisitesCreateSerializer(data=request.data)
        data_valid = serializer.is_valid()
        if not data_valid:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.query_params.get('save'):
            serializer.save(client=client)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_200_OK)
