from .models import Client
from .serializers import (ClientSerializer,
                          ClientLoginSerializer,
                          ClientUpdateSerializer,
                          ClientPasswordResetSerializer)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import (permission_classes,
                                       authentication_classes)
from rest_framework.authentication import SessionAuthentication


class ClientRegistrationView(APIView):
    """
    Регистрация клиента.
    Доступно всем.
    """
    @swagger_auto_schema(
        tags=['client_tag'],
        operation_summary='Create client',
        request_body=ClientSerializer(),
        responses={
            status.HTTP_201_CREATED: ClientSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Invalid data',
        }
    )
    @permission_classes([AllowAny])
    def post(self, request):

        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientInfoView(APIView):
    """
    Получение данных о клиенте, направившем get запрос.
    Обновление сведений о клиенте, направившим запрос patch.
    Требует авторизации.
    """
    @swagger_auto_schema(
        tags=['client_tag'],
        operation_summary='Get client info',
        responses={
            status.HTTP_200_OK: ClientSerializer(),
            status.HTTP_401_UNAUTHORIZED: 'User not authenticated'
        }
    )
    @authentication_classes([SessionAuthentication])
    @permission_classes([IsAuthenticated])
    def get(self, request):

        # Получение информации о клиенте по идентификатору пользователя
        client = Client.objects.get(pk=request.user.pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['client_tag'],
        operation_summary='Update client (PATCH)',
        request_body=ClientSerializer(),
        responses={
            status.HTTP_200_OK: ClientSerializer(),
            status.HTTP_400_BAD_REQUEST: 'Invalid data',
            status.HTTP_401_UNAUTHORIZED: 'User not authenticated'
        }
    )
    @authentication_classes([SessionAuthentication])
    @permission_classes([IsAuthenticated])
    def patch(self, request):
        # Получение объекта клиента по идентификатору пользователя
        client = Client.objects.get(pk=request.user.pk)
        # Указание partial=True для частичного обновления
        serializer = ClientUpdateSerializer(client,
                                            data=request.data,
                                            partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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

            user = authenticate(request=request,
                                phone=phone,
                                password=password)

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
        responses={
            status.HTTP_200_OK: "'message':'Logged out successfully'",
            status.HTTP_401_UNAUTHORIZED: "'message':'User not authenticated'",
        }
    )
    @authentication_classes([SessionAuthentication])
    @permission_classes([IsAuthenticated])
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response(
                {'message': 'Logged out successfully'},
                status=status.HTTP_200_OK)
        return Response(
            {'message': 'User not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED)


# восстановление пароля
class ClientPasswordResetView(APIView):
    """
    Восстановление пароля клиента на основе телефона и нового пароля.
    """
    @permission_classes([AllowAny])
    @swagger_auto_schema(
        tags=['client_tag'],
        operation_summary='Password reset',
        request_body=ClientPasswordResetSerializer(),
        responses={
            status.HTTP_200_OK:
            "{'message': 'Password reset successfully'}",
            status.HTTP_404_NOT_FOUND:
            "{'message': 'Client with this phone does not exist'}",
        }
    )
    def post(self, request):
        serializer = ClientPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get('phone')
            new_password = serializer.validated_data.get('new_password')
            try:
                client = Client.objects.get(phone=phone)
                client.set_password(new_password)
                client.save(update_fields=['password'])
                return Response({'message': 'Password reset successfully'},
                                status=status.HTTP_200_OK)
            except Client.DoesNotExist:
                return Response(
                    {'message': 'Client with this phone does not exist'},
                    status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
