from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Model
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.routers import APIRootView


class IsOwnerOrAdminOrReadOnly(BasePermission):
    """
    Анонимным пользователям разрешен просмотр.
    Администратору или автору рецепта разрешены
    остальные методы.
    """
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (obj.author == request.user
                or request.user.is_superuser)


class OwnerUserOrReadOnly(BasePermission):
    """
    Администратору и авторизованному пользователю разрешены создание
    и изменение рецептов. Анонимному пользователю только просмотр.
    """

    def has_object_permission(
        self, request: WSGIRequest, view: APIRootView, obj: Model
    ) -> bool:
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and request.user == obj.author
            or request.user.is_staff
        )
