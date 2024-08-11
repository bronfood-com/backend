from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, viewsets, serializers, generics
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
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
    Basket,
)

from .serializers import (
    MealSerializer,
    MenuSerializer,
    RestaurantSerializer,
    TagSerializer,
    OrderSerializer,
    OrderedMealSerializer,
    CoordinatesSerializer,
    ChoiceSerializer,
    FavoritesSerializer,
    MealInBasketSerializer,
    BasketSerializer,
    FeatureSerializer,
    RestaurantMenuSerializer,
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
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorites.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        restaurant = Restaurant.objects.get(id=self.request.data["restaurant"])
        if Favorites.objects.filter(
            user=self.request.user, restaurant=restaurant
        ).exists():
            raise serializers.ValidationError("Ресторан уже в избранном")
        serializer.save(user=self.request.user, restaurant=restaurant)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"status": "success", "message": "Ресторан удален из избранного"}
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "status": "success",
                "message": "Ресторан добавлен в избранное",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class MealInBasketViewSet(viewsets.ModelViewSet):
    queryset = MealInBasket.objects.all()
    serializer_class = MealInBasketSerializer


def serialize_basket(basket):
    restaurant_data = (
        RestaurantSerializer(basket.restaurant).data if basket.restaurant else {}
    )
    meals_data = [
        {
            "count": meal_in_basket.count,
            "meal": MealSerializer(meal_in_basket.meal).data,
        }
        for meal_in_basket in basket.meals.all()
    ]
    return {"restaurant": restaurant_data, "meals": meals_data}


@api_view(["POST"])
def empty_basket(request):
    user = request.user
    try:
        basket = Basket.objects.get(user=user)
        basket.meals.clear()
        basket.restaurant = None
        basket.save()
        return Response({"data": serialize_basket(basket)}, status=status.HTTP_200_OK)
    except Basket.DoesNotExist:
        return Response(
            {"error": "Корзина не найдена"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
def get_basket_ex(request):
    user = request.user.id
    if user:
        basket = Basket.objects.get(user=user)
        serializer = BasketSerializer(basket)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def add_meal_to_basket(request):
    user = request.user
    restaurant_id = request.data.get("restaurant_id")
    meal_id = request.data.get("meal_id")

    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        meal = Meal.objects.get(id=meal_id)
        feature_meal_requested = meal.features.get()
        print(f"{feature_meal_requested=}")
    except (Restaurant.DoesNotExist, Meal.DoesNotExist):
        return Response(
            {"error": "Restaurant or Meal not found"}, status=status.HTTP_404_NOT_FOUND
        )
    basket, created = Basket.objects.get_or_create(
        user=user, defaults={"restaurant": restaurant}
    )

    if not created and basket.restaurant != restaurant:
        basket.restaurant = restaurant
        basket.save()

    meal_in_basket, created = MealInBasket.objects.get_or_create(
        meal=meal, defaults={"count": 0}
    )
    print(f"{meal_in_basket=}")

    feature_meal_basket = meal_in_basket.meal.features.get()
    print(f"{feature_meal_basket=}")
    if feature_meal_basket == feature_meal_requested:
        meal_in_basket.count += 1
    else:
        meal_in_basket.count = 1

    meal_in_basket.save()
    basket.meals.add(meal_in_basket)
    basket.save()

    basket = Basket.objects.get(user=user)
    serializer = BasketSerializer(basket, context={"request": request})
    return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def delete_meal_from_basket(request):
    user = request.user
    meal_id = request.data.get("meal_id")

    try:
        meal_in_basket = MealInBasket.objects.get(meal_id=meal_id, baskets__user=user)
        if meal_in_basket.count > 1:
            meal_in_basket.count -= 1
            meal_in_basket.save()
            message = "Количество блюда уменьшено"
        else:
            meal_in_basket.delete()
            message = "Блюдо удалено из корзины"

        basket = Basket.objects.get(user=user)
        serializer = BasketSerializer(basket, context={"request": request})
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    except MealInBasket.DoesNotExist:
        return Response(
            {"error": "Блюдо не найдено в корзине"}, status=status.HTTP_404_NOT_FOUND
        )
    except Basket.DoesNotExist:
        return Response(
            {"error": "Корзина не найдена"}, status=status.HTTP_404_NOT_FOUND
        )


class RestaurantViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Restaurant.objects.all()
        serializer = RestaurantSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response({"status": "success", "data": serializer.data})

    def retrieve(self, request, pk=None):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            serializer = RestaurantSerializer(restaurant, context={"request": request})
            return Response({"status": "success", "data": serializer.data})
        except Restaurant.DoesNotExist:
            return Response(
                {"status": "error", "error_message": "Ошибка сервера"}, status=404
            )

    @action(detail=True, methods=["get"], url_path="menu")
    def restaurant_meals(self, request, pk=None):
        """
        Возвращает список блюд указанного ресторана.
        """
        restaurant = get_object_or_404(Restaurant, pk=pk)
        menus = Menu.objects.filter(restaurant=restaurant)
        serializer = RestaurantMenuSerializer(
            menus, many=True, context={"request": request}
        )

        for menu in serializer.data:
            if "id" in menu:
                del menu["id"]
            if "restaurant" in menu:
                del menu["restaurant"]

        return Response({"meals": serializer.data})


def restaurant_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu = restaurant.menu_set.all().values("meals")

    # Преобразуем данные меню
    menu_data = []
    for item in menu:
        meals = item["meals"]
        for meal in meals:
            meal.pop("id", None)
        menu_data.append({"meals": meals, "restaurant": restaurant_id})

    return JsonResponse(menu_data, safe=False)


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
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

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

    @action(detail=True, methods=["post"])
    def confirm_order(self, request, pk=None):
        order = self.get_object()
        order.admin_confirmed = True
        order.save()
        return Response({"status": "Заказ подтвержден"})

    @action(detail=True, methods=["get"])
    def check_order_status(self, request, pk=None):
        order = self.get_object()
        now = timezone.now()
        if order.admin_confirmed:
            return Response({"status": "Заказ подтвержден"})
        elif order.preparation_end_time and now > order.preparation_end_time:
            elapsed_time = now - order.preparation_end_time
            return Response(
                {
                    "status": f"Время подготовки истекло {elapsed_time.seconds} секунд назад"
                }
            )
        else:
            remaining_time = order.preparation_end_time - now
            return Response(
                {
                    "status": f"Осталось {remaining_time.seconds} секунд до окончания времени подготовки"
                }
            )


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


class RestaurantMenuView(generics.ListAPIView):
    serializer_class = RestaurantMenuSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs["restaurant_id"]
        return Menu.objects.filter(restaurant_id=restaurant_id)


@api_view(["GET"])
def restaurant_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    serializer = RestaurantMenuSerializer(restaurant)
    return Response(serializer.data)
