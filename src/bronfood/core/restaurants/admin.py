from django.contrib import admin  # noqa
from .models import (
    Restaurant, Menu, Meal, Tag, Feature,
    Coordinates, Choice, Favorites, MealInBasket,
    Basket, OrderedMeal, Order
)

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Meal)
admin.site.register(Tag)
admin.site.register(Feature)
admin.site.register(Coordinates)
admin.site.register(Choice)
admin.site.register(Favorites)
admin.site.register(MealInBasket)
admin.site.register(Basket)
admin.site.register(OrderedMeal)
admin.site.register(Order)
