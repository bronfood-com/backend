from rest_framework import permissions


class IsAuthenticatedConfirmedMixin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.status == 'Confirmed'
        )

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAuthenticatedRestaurantOwner(IsAuthenticatedConfirmedMixin):
    """ Класс определеня прав для владельца ресторана."""
    def has_permission(self, request, view):
        return super().has_permission() and request.user.role == 'owner'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAuthenticatedRestaurantAdmin(IsAuthenticatedConfirmedMixin):
    """ Класс определеня прав для администратора ресторана."""
    def has_permission(self, request, view):
        return (
            super().has_permission()
            and request.user.role == 'restaurant_admin'
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in ('GET', 'PUT', 'UPDATE')
            and obj.user == request.user
        )


class IsAuthenticatedClient(IsAuthenticatedConfirmedMixin):
    """ Класс определеня прав для клиента ресторана/заведения."""
    def has_permission(self, request, view):
        return super().has_permission() and request.user.role == 'client'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
