from rest_framework.generics import CreateAPIView
from .models import Client
from .serializers import Client, ClientSerializer, ClientLoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout


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


class ClientLoginView(APIView):

    serializer_class = ClientLoginSerializer

    @swagger_auto_schema(
        tags=['client_tag'],
        operation_summary='Create login',
        request_body=ClientLoginSerializer(),
        responses={
            status.HTTP_200_OK: "{'message': 'Logged in successfully'}",
            status.HTTP_401_UNAUTHORIZED: 'Invalid credentials',
            status.HTTP_400_BAD_REQUEST: 'Invalid data'
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get('phone')
            password = serializer.validated_data.get('password')

            user = authenticate(request=request, phone=phone, password=password)

            if user:
                login(request, user)
                return Response(
                    {'message': 'Logged in successfully'},
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    {'message': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientLogoutView(APIView):
    @swagger_auto_schema(
        tags=['client_tag'],
        operation_summary='Logout',
        # request_body=ClientLoginSerializer(),
        responses={
            status.HTTP_200_OK: "{'message': 'Logged out successfully'}",
            status.HTTP_401_UNAUTHORIZED: 'User not authenticated',
        }
    )
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response(
                {'message': 'Logged out successfully'},
                status=status.HTTP_200_OK)
        return Response(
            {'message': 'User not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED)
