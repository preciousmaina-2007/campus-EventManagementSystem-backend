from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Allow access only to ADMIN users."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "ADMIN"
        )


class IsOrganizer(BasePermission):
    """Allow access only to ORGANIZER users."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "ORGANIZER"
        )
