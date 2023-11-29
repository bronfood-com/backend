from django.contrib import admin  # noqa
from .models import Restaurant, Menu, Dishes, Tag


admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Dishes)
admin.site.register(Tag)
