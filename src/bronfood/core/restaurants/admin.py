from django.contrib import admin  # noqa
from .models import Restaurant, Menu


admin.site.register(Restaurant)
admin.site.register(Menu)
