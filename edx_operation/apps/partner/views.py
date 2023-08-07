from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from edx_operation.apps.partner.serializers import (
    PartnerCSerializer,
    PartnerEnrollmentCSerializer,
    PartnerEnrollmentSerializer,
    PartnerSerializer,
    PartnerStudentCSerializer,
    PartnerStudentSerializer,
)
from edx_operation.apps.partner.models import Partner, PartnerEnrollment, PartnerStudent


class PermissionMixin:
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class DisableMethodMixin:
    def create(self, request, *args, **kwargs):
        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, *args, **kwargs):
        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PartnerViewSet(DisableMethodMixin, PermissionMixin, viewsets.ModelViewSet):
    queryset = Partner.objects.all().order_by("-created")
    serializer_class = PartnerSerializer

    @action(detail=False, methods=["post"], serializer_class=PartnerCSerializer)
    def join(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Partner.join(**serializer.data)
        return Response(serializer.data)


class PartnerStudentViewSet(DisableMethodMixin, PermissionMixin, viewsets.ModelViewSet):
    queryset = PartnerStudent.objects.all().order_by("-created")
    serializer_class = PartnerStudentSerializer

    @action(detail=False, methods=["post"], serializer_class=PartnerStudentCSerializer)
    def link(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        PartnerStudent.link(**serializer.data)
        return Response(serializer.data)


class PartnerEnrollmentViewSet(DisableMethodMixin, PermissionMixin, viewsets.ModelViewSet):
    queryset = PartnerEnrollment.objects.all().order_by("-created")
    serializer_class = PartnerEnrollmentSerializer

    @action(detail=False, methods=["post"], serializer_class=PartnerEnrollmentCSerializer)
    def enroll(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        PartnerEnrollment.enroll(**serializer.data)
        return Response(serializer.data)
