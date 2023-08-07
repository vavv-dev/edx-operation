from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from edx_operation.apps.grade.serializers import (
    CourseGradeSerializer,
)
from edx_operation.apps.grade.models import CourseGrade


class PermissionMixin:
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class DisableMethodMixin:
    def create(self, request, *args, **kwargs):
        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, *args, **kwargs):
        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CourseGradeViewSet(DisableMethodMixin, PermissionMixin, viewsets.ModelViewSet):
    queryset = CourseGrade.objects.all().order_by("-created")
    serializer_class = CourseGradeSerializer
