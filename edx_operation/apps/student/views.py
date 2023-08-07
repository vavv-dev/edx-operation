from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from edx_operation.apps.student.serializers import (
    StudentCSerializer,
    StudentSerializer,
)
from edx_operation.apps.student.models import Student


class PermissionMixin:
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class DisableMethodMixin:
    def create(self, request, *args, **kwargs):
        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, *args, **kwargs):
        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class StudentViewSet(DisableMethodMixin, PermissionMixin, viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by("-created")
    serializer_class = StudentSerializer

    @action(detail=False, methods=["post"], serializer_class=StudentCSerializer)
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Student.register(**serializer.data)
        return Response(serializer.data)
