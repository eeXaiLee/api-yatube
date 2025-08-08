from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from posts.models import Comment, Group, Post

from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    Реализация работы с постами.

    Атрибуты:
        queryset: Все объекты Post.
        serializer_class: Сериализатор для Post.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer) -> None:
        """
        Сохраняет пост с текущим пользователем как автором.

        Args:
            serializer: Сериализатор данных для создания объекта.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer) -> None:
        """
        Обновляет пост, если текущий пользователь - автор.

        Args:
            serializerСериализатор данных для обновления объекта.

        Raises:
            PermissionDenied: Если текущий пользователь не является
            автором поста.
        """
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                'Вы не можете редактировать чужой пост.'
            )
        serializer.save()

    def perform_destroy(self, instance) -> None:
        """
        Удаляет пост, если текущий пользователь - автор.

        Args:
            instance: Экземпляр поста для удаления.

        Raises:
            PermissionDenied: Если текущий пользователь не является
            автором поста.
        """
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Вы не можете удалить чужой пост.'
            )
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Реализация просмотра групп.

    Атрибуты:
        queryset: Все объекты Group.
        serializer_class: Сериализатор для Group.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    Реализация работы с комментариями.

    Атрибуты:
        queryset: Все объекты Comment.
        serializer_class: Сериализатор для Comment.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_post(self) -> Post:
        """
        Получить объект Post по параметру URL post_id.

        Returns:
            Post: Объект поста, связанный с комментариями.

        Raises:
            Http404: Если пост с указанным ID не найден.
        """
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self) -> QuerySet[Comment]:
        """
        Получить queryset комментариев, относящихся к текущему посту.

        Returns:
            QuerySet: QuerySet комментариев поста.
        """
        return self.get_post().comments.all()

    def perform_create(self, serializer) -> None:
        """
        Сохраняет комментарий с текущим пользователем как автором и
        связывает с постом.

        Args:
            serializer: Сериализатор данных для создания объекта.
        """
        serializer.save(author=self.request.user, post=self.get_post())

    def perform_update(self, serializer) -> None:
        """
        Обновляет комментарий, если текущий пользователь - автор.

        Args:
            serializer: Сериализатор данных для обновления объекта.

        Raises:
            PermissionDenied: Если текущий пользователь не является
            автором комментария.
        """
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                'Вы не можете редактировать чужой комментарий.'
            )
        serializer.save()

    def perform_destroy(self, instance) -> None:
        """
        Удаляет комментарий, если текущий пользователь - автор.

        Args:
            instance: Экземпляр комментария для удаления.

        Raises:
            PermissionDenied: Если текущий пользователь не является
            автором комментария.
        """
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Вы не можете удалить чужой комментарий.'
            )
        instance.delete()
