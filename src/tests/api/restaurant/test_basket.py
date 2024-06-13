from django.test import TestCase

# from bronfood.core.restaurants.models import Basket, MealInBasket
from bronfood.api.restaurants.serializers import BasketSerializer


class BasketSerializerTest(TestCase):

    def test_valid_create_basket_with_meals(self):
        """Тест на создание корзины из полных наименований."""
        data = {
            'restaurant': 'Test Restaurant',
            'meals': [
                {'name': 'Meal 1', 'quantity': 2},
                {'name': 'Meal 2', 'quantity': 1}
            ]
        }
        serializer = BasketSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        basket = serializer.save()

        self.assertEqual(basket.restaurant, 'Test Restaurant')
        self.assertEqual(basket.meals.count(), 2)

        meal_names = [meal.name for meal in basket.meals.all()]
        self.assertIn('Meal 1', meal_names)
        self.assertIn('Meal 2', meal_names)

    def test_invalid_create_basket_missing_required_field(self):
        """Тест что корзину нельзя создать из неполных блюд."""
        data = {
            'meals': [
                {'name': 'Meal 1', 'quantity': 2}
            ]
        }
        serializer = BasketSerializer(data=data)
        self.assertFalse(serializer.is_valid())
