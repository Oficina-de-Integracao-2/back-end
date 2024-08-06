from rest_framework import permissions
from rest_framework.views import Request, View
from professor.models import Professor


class IsAdminOrProfessorOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Professor):
        return request.user.is_superuser or request.user.id == obj.id
