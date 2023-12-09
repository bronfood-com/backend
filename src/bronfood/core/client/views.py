from rest_framework.generics import CreateAPIView
from .models import Client
from .serializers import Client, ClientSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView


# class CreateClient(CreateAPIView):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer
#     permission_classes = [AllowAny]  # Пермишен для проверки аутентификации

#     def post(self, request, *args, **kwargs):
#         return super().post(request, *args, **kwargs)
    # Дополнительная логика, если требуется
    # Например, переопределение метода perform_create для управления созданием объекта
    # def perform_create(self, serializer):
    #     # Добавление дополнительных данных перед сохранением объекта
    #     serializer.save(user=self.request.user) 


class ClientAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['client_tag'],
        operation_summary='Create client',
        request_body=ClientSerializer(),
        responses={
            status.HTTP_201_CREATED: ClientSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Invalid data',
        }
    )
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
