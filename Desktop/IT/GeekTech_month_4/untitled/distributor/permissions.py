from rest_framework.permissions import BasePermission

from distributor.models import ADMIN


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.profile.role == ADMIN)
