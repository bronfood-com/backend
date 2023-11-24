from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def healthcheck(request):
    """отправляет get запрос на /healthcheck/,
    возвращает статус 200 с json {"message": "ok"}"""
    return Response({'message': 'ok'}, status=status.HTTP_200_OK)
