from rest_framework.permissions import BasePermission


class IsOrganizer(BasePermission):
    """
    Allows access only to users with ORGANIZER role
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "ORGANIZER"
        )


class IsOwnerOrReadOnly(BasePermission):
    """
    Users can view events.
    Only the organizer who created the event can edit/delete.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return obj.organizer == request.user