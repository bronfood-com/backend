from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bronfood.api.client.utils import error_data, success_data
from bronfood.api.views import BaseAPIView
from bronfood.api.review.serializers import (
    ReviewSerializer, RestaurantReviewSerializer
)
from bronfood.core.restaurants.models import Restaurant
from decimal import Decimal


class ReviewCreateAPIView(BaseAPIView):
    """
    Создание отзыва о ресторане.
    Включает в себя формирование общего рейтинга ресторана.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, restaurant_id, *args, **kwargs):
        data = request.data
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response(
                data=error_data('RestaurantNotFoundError'),
                status=status.HTTP_404_NOT_FOUND
            )
        data['restaurant'] = restaurant_id

        serializer = ReviewSerializer(data=data)

        if serializer.is_valid():

            serializer.save(client=self.request.user)
            rating = request.data['rating']
            if restaurant.rating is None:
                restaurant.rating = rating
            else:
                restaurant.rating = (restaurant.rating + Decimal(rating)) / 2
            restaurant.save()
            return Response(success_data(None),
                            status=status.HTTP_200_OK)

        return Response(
            data=error_data('ValidationError'),
            status=status.HTTP_400_BAD_REQUEST)


class RestaurantReviewAPIView(BaseAPIView):
    """
    Получение отзывов о ресторане.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, restaurant_id, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response(
                data=error_data('RestaurantNotFoundError'),
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RestaurantReviewSerializer(restaurant)
        return Response(
            success_data(serializer.data),
            status=status.HTTP_200_OK
        )
