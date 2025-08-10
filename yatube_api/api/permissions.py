from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Проверяет, является ли пользователь автором объекта для полного доступа.

    Разрешает полный доступ (GET, HEAD, OPTIONS) для всех пользователей.
    Разрешает изменение и удаление только автору объекта.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
