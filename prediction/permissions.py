from rest_framework import permissions


class IsAdminUser(permissions.IsAdminUser):
    """
    Object-level permission to only allow admins to edit / delete it.
    """

    def has_permission(self, request, view):
        # Always allow GET, HEAD or OPTIONS requests.
        if request.user.is_authenticated and request.user.is_superuser:
            return True

        return False


class IsAuthenticatedUser(permissions.IsAdminUser):
    """
    Object-level permission to only allow admins to edit / delete it.
    """

    def has_permission(self, request, view):
        # Always allow GET, HEAD or OPTIONS requests.
        if request.user.is_authenticated:
            return True

        return False
