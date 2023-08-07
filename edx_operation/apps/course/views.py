from django.conf import settings
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from edx_operation.apps.course.models import Course, CourseAccessRole
from edx_operation.apps.course.serializers import (
    CourseAccessRoleASerializer,
    CourseAccessRoleSerializer,
    CourseCSerializer,
    CourseISerializer,
    CourseSerializer,
)


class PermissionMixin:
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class DisableMethodMixin:
    def create(self, request, *args, **kwargs):
        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, *args, **kwargs):
        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CourseViewSet(DisableMethodMixin, PermissionMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by("-created")
    serializer_class = CourseSerializer

    @action(detail=False, methods=["post"], serializer_class=CourseISerializer)
    def import_olx(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # olx file
        data = serializer.data
        data.update(olx=request.FILES.get("olx"))

        Course.import_olx(**data)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], serializer_class=CourseCSerializer)
    def rerun(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Course.rerun(**serializer.data)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def blocks(self, request, *args, **kwargs):
        instance = self.get_object()

        # action
        instance.sync_course_blocks()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CourseAccessRoleViewSet(DisableMethodMixin, PermissionMixin, viewsets.ModelViewSet):
    queryset = CourseAccessRole.objects.all().order_by("-created")
    serializer_class = CourseAccessRoleSerializer

    @action(detail=False, methods=["post"], serializer_class=CourseAccessRoleASerializer)
    def allow(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        CourseAccessRole.allow(request, **serializer.data)
        return Response(serializer.data)
