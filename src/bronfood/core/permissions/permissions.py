from rest_framework import permissions


class IsAuthenticatedRestaurantOwner(permissions.BasePermission):
    """ Класс определеня прав для владельца ресторана."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role.OWNER
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role.OWNER
        )


class IsAuthenticatedRestaurantAdmin(permissions.BasePermission):
    """ Класс определеня прав для администратора ресторана."""
    def has_permission(self, request, view):
        return (
            request.method in ('GET', 'PUT', 'UPDATE')
            and request.user.role.RESTAURANT_ADMIN
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role.RESTAURANT_ADMIN
        )


class IsAuthenticatedClient(permissions.BasePermission):
    """ Класс определеня прав для клиента ресторана/заведения."""
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role.CLIENT
        )
