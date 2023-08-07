from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from edx_operation.apps.enrollment.models import Enrollment
from edx_operation.apps.enrollment.serializers import (
    EnrollmentCSerializer,
    EnrollmentSerializer,
)


class PermissionMixin:
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class DisableMethodMixin:
    def create(self, request, *args, **kwargs):
        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, *args, **kwargs):
        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class EnrollmentViewSet(DisableMethodMixin, PermissionMixin, viewsets.ModelViewSet):
    queryset = Enrollment.objects.all().order_by("-created")
    serializer_class = EnrollmentSerializer

    @action(detail=False, methods=["post"], serializer_class=EnrollmentCSerializer)
    def enroll(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Enrollment.enroll(**serializer.data)
        return Response(serializer.data)
