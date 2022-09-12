from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .permissions import AuthorOrReadOnly
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer
)
from posts.models import Post, Group


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in [
            'update',
            'partial_update',
            'destroy'
        ]:
            return (AuthorOrReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in [
            'update',
            'partial_update',
            'destroy'
        ]:
            return (AuthorOrReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(
            post=post,
            author=self.request.user)
