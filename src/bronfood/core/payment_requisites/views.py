from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bronfood.core.payment_requisites.models import PaymentRequisites
from bronfood.core.payment_requisites.serializers import PaymentRequisitesCreateSerializer
from bronfood.core.client.models import Client


class PaymentRequisitesView(APIView):

    def post(self, request, user_id, format=None):
        print(format)
        print(request.query_params)
        print(user_id)
        client = get_object_or_404(Client, id=user_id)
        user = request.user
        print(user)
        serializer = PaymentRequisitesCreateSerializer(data=request.data)
        if request.query_params.get('save') and serializer.is_valid():
            serializer.save(client=client)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
