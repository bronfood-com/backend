from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from bronfood.api.client.utils import success_data, error_data
from bronfood.core.client.models import Client, UserAccount
from bronfood.api.client.serializers import ClientLoginSerializer


@api_view(['GET'])
def healthcheck(request):
    """отправляет get запрос на /healthcheck/,
    возвращает статус 200 с json {"message": "ok"}"""
    return Response({'message': 'ok'}, status=status.HTTP_200_OK)


class BaseAPIView(APIView):

    @property
    def current_client(self) -> Client | None:
        return Client.objects.get(pk=self.request.user.pk)


class CustomTokenCreateView(APIView):
    """
    Token creation view.
    """
    serializer_class = ClientLoginSerializer

    def post(self, request):
        user_signin_serializer = self.serializer_class(data=request.data)
        if not user_signin_serializer.is_valid():
            return Response(
                data=error_data('invalidCredentials'),
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # нахожу пользователя
            user = UserAccount.objects.get(phone=request.data['phone'])
            # проверяю передан ли пароль пользователя
            if not check_password(request.data['password'],
                                  user.password):
                raise Exception
        except Exception:
            return Response(
                data=error_data('invalidCredentials'),
                status=status.HTTP_400_BAD_REQUEST
            )
        # присваиваю пользователю токен
        token, created = Token.objects.get_or_create(user=user)
        # отдаю результата
        data = {
            'fullname': token.user.fullname,
            'phone': token.user.phone,
            'role': token.user.role,
            'auth_token': token.key
        }
        return Response(success_data(data),
                        status=status.HTTP_200_OK)
