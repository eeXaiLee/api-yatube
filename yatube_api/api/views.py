from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from posts.models import Comment, Group, Post

from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    Реализация работы с постами.

    Атрибуты:
        queryset: Все объекты Post.
        serializer_class: Сериализатор для Post.
        permission_classes: Права доступа.
    """

    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer) -> None:
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Реализация просмотра групп.

    Атрибуты:
        queryset: Все объекты Group.
        serializer_class: Сериализатор для Group.
        permission_classes: Права доступа.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    """
    Реализация работы с комментариями.

    Атрибуты:
        queryset: Все объекты Comment.
        serializer_class: Сериализатор для Comment.
        permission_classes: Права доступа.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

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
        Возвращаем комментарии, отфильтрованные по post_id.

        Returns:
            QuerySet: QuerySet комментариев поста.
        """
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id).select_related('author')

    def perform_create(self, serializer) -> None:
        serializer.save(author=self.request.user, post=self.get_post())
