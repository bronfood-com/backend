from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import RestaurantOwner


@admin.register(RestaurantOwner)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'phone')
    list_filter = ('email', 'username', 'phone')
