from rest_framework import serializers
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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class OrderedMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedMeal
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    orderedMeal = OrderedMealSerializer()

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        ordered_meal_data = validated_data.pop("orderedMeal")
        ordered_meal = OrderedMeal.objects.create(**ordered_meal_data)
        order = Order.objects.create(
            orderedMeal=ordered_meal,
            **validated_data
        )
        return order

    def update(self, instance, validated_data):
        ordered_meal_data = validated_data.pop("orderedMeal", {})
        ordered_meal = instance.orderedMeal

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        for attr, value in ordered_meal_data.items():
            setattr(ordered_meal, attr, value)

        ordered_meal.save()
        instance.save()

        return instance


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = ["latitude", "longitude"]


class RestaurantSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    coordinates = CoordinatesSerializer(read_only=True)
    type = serializers.ChoiceField(choices=Restaurant.RESTAURANT_TYPES)

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "name",
            "photo",
            "address",
            "isLiked",
            "coordinates",
            "rating",
            "workingTime",
            "type",
        ]

    def get_photo(self, obj):
        request = self.context.get("request")
        if request and obj.photo:
            return request.build_absolute_uri(obj.photo)
        return None


class ChoiceSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False
    )

    class Meta:
        model = Choice
        fields = ["id", "name", "price", "default", "chosen"]


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class MealSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False
    )

    class Meta:
        model = Meal
        fields = "__all__"


class MealInBasketSerializer(serializers.ModelSerializer):
    meal = MealSerializer(read_only=True)

    class Meta:
        model = MealInBasket
        fields = ["meal", "count"]


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = "__all__"


class MenuSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True)

    class Meta:
        model = Menu
        fields = ["meals"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["data"] = representation.pop("meals")
        return representation


class BasketSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()
    meals = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ["id", "user", "restaurant", "meals"]

    def get_meals(self, obj):
        return [
            {
                "count": meal_in_basket.count,
                "meal": MealSerializer(meal_in_basket.meal).data,
            }
            for meal_in_basket in obj.meals.all()
        ]


class RestaurantMenuSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ["meals"]
