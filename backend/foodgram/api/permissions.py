from rest_framework.permissions import SAFE_METHODS, BasePermission


class OwnerUserOrReadOnly(BasePermission):
    """
    Администратору и авторизованному пользователю разрешены создание
    и изменение рецептов. Анонимному пользователю только просмотр.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user == obj.author or request.user.admin)


class AdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.admin
        )
