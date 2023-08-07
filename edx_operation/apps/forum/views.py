from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from edx_operation.apps.forum.models import Post

from edx_operation.apps.forum.serializers import PostSerializer


class PermissionMixin:
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class DisableMethodMixin:
    def create(self, request, *args, **kwargs):
        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, *args, **kwargs):
        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PostViewSet(DisableMethodMixin, PermissionMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
