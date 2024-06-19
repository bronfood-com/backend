from django.http import Http404
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from bronfood.core.restaurants.models import (
    Meal,
    Menu,
    Restaurant,
    Tag,
    Order,
    OrderedMeal,
    Coordinates,
    Choice,
    Feature,
    Favorites,
    MealInBasket,
    Basket
)

from .serializers import (
    MealSerializer,
    MenuSerializer,
    RestaurantListSerializer,
    RestaurantDetailSerializer,
    TagSerializer,
    OrderSerializer,
    OrderedMealSerializer,
    CoordinatesSerializer,
    ChoiceSerializer,
    FavoritesSerializer,
    MealInBasketSerializer,
    BasketSerializer,
    FeatureSerializer
)


class CoordinatesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coordinates.objects.all()
    serializer_class = CoordinatesSerializer


class ChoiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class FeatureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer


class MealInBasketViewSet(viewsets.ModelViewSet):
    queryset = MealInBasket.objects.all()
    serializer_class = MealInBasketSerializer


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return RestaurantListSerializer
        else:
            return RestaurantDetailSerializer


class MenuViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class MealViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer


class OrderedMealViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrderedMeal.objects.all()
    serializer_class = OrderedMealSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def confirm_order(self, request, pk=None):
        order = self.get_object()
        order.admin_confirmed = True
        order.save()
        return Response({'status': 'Заказ подтвержден'})

    @action(detail=True, methods=['get'])
    def check_order_status(self, request, pk=None):
        order = self.get_object()
        now = timezone.now()
        if order.admin_confirmed:
            return Response({'status': 'Заказ подтвержден'})
        elif order.preparation_end_time and now > order.preparation_end_time:
            elapsed_time = now - order.preparation_end_time
            return Response({'status': f'Время подготовки истекло {elapsed_time.seconds} секунд назад'})
        else:
            remaining_time = order.preparation_end_time - now
            return Response({'status': f'Осталось {remaining_time.seconds} секунд до окончания времени подготовки'})


class RestaurantMeals(APIView):
    def get_object(self, pk):
        try:
            return Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        restaurant = self.get_object(pk)
        serializer = MealSerializer(restaurant.meals.all(), many=True)
        return Response(serializer.data)


class RestaurantMealDetail(APIView):
    def get_object(self, restaurant_id, meal_id):
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            return Meal.objects.get(pk=meal_id, restaurant=restaurant)
        except Restaurant.DoesNotExist:
            raise Http404
        except Meal.DoesNotExist:
            raise Http404

    def get(self, request, restaurant_id, meal_id, format=None):
        meal = self.get_object(restaurant_id, meal_id)
        serializer = MealSerializer(meal)
        return Response(serializer.data)


class UserFavoritesView(APIView):
    def get(self, request, user_id):
        favorites = Favorites.objects.filter(user_id=user_id)
        favorite_restaurants = Restaurant.objects.filter(
            id__in=[favorite.restaurant_id for favorite in favorites]
        )
        serializer = RestaurantDetailSerializer(favorite_restaurants, many=True)
        return Response({"status": "success", "data": serializer.data})


class DeleteUserFavoriteView(APIView):
    def delete(self, request, user_id, restaurant_id):
        favorite = Favorites.objects.filter(user_id=user_id, restaurant_id=restaurant_id)
        if favorite.exists():
            favorite.delete()
            return Response({"status": "success"})
        else:
            return Response({"status": "error", "error_message": "Избранное не найдено"})


class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
