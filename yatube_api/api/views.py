from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from posts.models import Follow, Group, Post, User
from .serializers import (PostSerializer, CommentSerializer,
                          GroupSerializer, FollowSerializer)
from .permissions import OwnerOrReadOnly, ReadOnly


class BaseViewSet(ModelViewSet):
    """Базовый ViewSet с общими методами."""
    permission_classes = (OwnerOrReadOnly,)

    def get_permissions(self):
        """Настройка прав доступа"""
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class PostViewSet(BaseViewSet):
    """Вьюсет для постов"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Создание нового поста"""
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    """Вьюсет для сообществ"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CommentViewSet(BaseViewSet):
    """Вьюсет для комментариев"""
    serializer_class = CommentSerializer

    def get_post(self):
        """Получения поста к которому относится комментарий"""
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Получение списка комментариев для поста"""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """Создание нового комментария"""
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(ModelViewSet):
    """Вьюсет для подписок"""
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Получение подписок пользователя"""
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Создание новой подписки"""
        username = self.request.data.get("following")
        following = get_object_or_404(User, username=username)

        filters = Follow.objects.filter(
            user=self.request.user, following=following).exists()
        if self.request.user == following:
            raise ValidationError("Нельзя подписаться на самого себя")
        if filters:
            raise ValidationError("Вы уже подписаны на этого пользователя")
        serializer.save(user=self.request.user, following=following)
