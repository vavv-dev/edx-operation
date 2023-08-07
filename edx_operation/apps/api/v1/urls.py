""" API v1 URLs. """

from django.urls import include, path
from rest_framework import routers

from edx_operation.apps.course.views import CourseAccessRoleViewSet, CourseViewSet
from edx_operation.apps.enrollment.views import EnrollmentViewSet
from edx_operation.apps.forum.views import PostViewSet
from edx_operation.apps.grade.views import CourseGradeViewSet
from edx_operation.apps.partner.views import (
    PartnerEnrollmentViewSet,
    PartnerStudentViewSet,
    PartnerViewSet,
)
from edx_operation.apps.student.views import StudentViewSet
from edx_operation.apps.notification.views import StudentNotificationViewSet


router = routers.DefaultRouter()
router.register(r"course", CourseViewSet)
router.register(r"courseaccessrole", CourseAccessRoleViewSet)
router.register(r"student", StudentViewSet)
router.register(r"enrollment", EnrollmentViewSet)
router.register(r"coursegrade", CourseGradeViewSet)
router.register(r"partner", PartnerViewSet)
router.register(r"partnerstudent", PartnerStudentViewSet)
router.register(r"partnerenrollment", PartnerEnrollmentViewSet)
router.register(r"studentnotification", StudentNotificationViewSet)
router.register(r"post", PostViewSet)


app_name = "v1"
urlpatterns = [
    path("", include(router.urls)),
]
