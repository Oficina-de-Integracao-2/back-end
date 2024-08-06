from rest_framework import permissions
from rest_framework.views import Request, View
from oficina.models import Oficina


class IsAdminOrProfessorOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Oficina):
        is_superuser = request.user.is_superuser
        is_owner = obj.professor == request.user
        return is_superuser or is_owner
