from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Проверяет, является ли пользователь модератором."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="moderators").exists()


class IsOwner(BasePermission):
    """Проверяет, является ли пользователь владельцем объекта."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.owner == request.user
