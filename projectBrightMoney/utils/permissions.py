from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            bool(
                request.user
                and request.user.is_authenticated
                and request.user.is_active
            )
            or request.user.is_superuser
        ):
            return True
        return False
