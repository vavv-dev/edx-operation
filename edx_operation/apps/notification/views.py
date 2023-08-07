from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from edx_operation.apps.notification.models import StudentNotification
from edx_operation.apps.notification.serializers import StudentNotificationSerializer


class PermissionMixin:
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class DisableMethodMixin:
    def create(self, request, *args, **kwargs):
        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, *args, **kwargs):
        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class StudentNotificationViewSet(DisableMethodMixin, PermissionMixin, viewsets.ModelViewSet):
    queryset = StudentNotification.objects.all().order_by("-id")
    serializer_class = StudentNotificationSerializer
