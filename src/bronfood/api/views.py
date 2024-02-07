from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from djoser import utils
from djoser.conf import settings
from djoser.views import TokenCreateView

from bronfood.core.client.models import Client
from bronfood.api.client.utils import success_data


@api_view(['GET'])
def healthcheck(request):
    """отправляет get запрос на /healthcheck/,
    возвращает статус 200 с json {"message": "ok"}"""
    return Response({'message': 'ok'}, status=status.HTTP_200_OK)


class BaseAPIView(APIView):

    @property
    def current_client(self) -> Client | None:
        return Client.objects.get(pk=self.request.user.pk)


class CustomTokenCreateView(TokenCreateView):
    """
    Custom token creation view with additional data.
    """
    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        response_data = token_serializer_class(token).data
        additional_data = {
            'fullname': token.user.fullname,
            'phone': token.user.phone,
            'role': token.user.role,
            }
        response_data.update(additional_data)
        return Response(success_data(response_data),
                        status=status.HTTP_200_OK)