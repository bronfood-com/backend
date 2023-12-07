from django.contrib import admin  # noqa
from .models import Restaurant, Menu, Dish, Tag


admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Dish)
admin.site.register(Tag)
