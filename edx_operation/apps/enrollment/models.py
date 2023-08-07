from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from edx_operation.apps.api_client.jwt import EnrollmentAPIClient
from edx_operation.apps.course.models import Course
from edx_operation.apps.student.models import Student


class Enrollment(TimeStampedModel):
    class Meta:
        verbose_name = _("Course Enrollment")
        verbose_name_plural = _("Course Enrollments")
        unique_together = (("course", "student"),)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mode = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True)

    @classmethod
    def enroll(cls, username, course_id, mode):
        payload = {
            "user": username,
            "course_details": {"course_id": str(course_id)},
            "mode": mode,
            "is_active": True,
            "force_enrollment": True,
        }

        EnrollmentAPIClient().v1_enrollment_create(payload)
