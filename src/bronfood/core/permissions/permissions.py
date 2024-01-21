from rest_framework import permissions


class IsAuthenticatedRestaurantOwner(permissions.BasePermission):
    """ Класс определеня прав для владельца ресторана."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'owner'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAuthenticatedRestaurantAdmin(permissions.BasePermission):
    """ Класс определеня прав для администратора ресторана."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'restaurant_admin'
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in ('GET', 'PUT', 'UPDATE')
            and obj.user == request.user
        )


class IsAuthenticatedClient(permissions.BasePermission):
    """ Класс определеня прав для клиента ресторана/заведения."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'client' 

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
