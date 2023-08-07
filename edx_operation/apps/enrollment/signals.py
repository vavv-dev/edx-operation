from django.dispatch import receiver

from edx_operation.apps.enrollment.models import Enrollment
from edx_operation.apps.event.kafka import OPERATION_EVENT_SIGNAL


@receiver(OPERATION_EVENT_SIGNAL)
def log_operation_event(event, **kwargs):
    if event.event_type == "operation_event.signals.courseenrollment":
        m = event.message

        Enrollment.objects.update_or_create(
            id=m.get("id"),
            defaults={
                "created": m.get("created"),
                "course_id": m.get("course_id"),
                "student_id": m.get("user_id"),
                "mode": m.get("mode"),
                "is_active": m.get("is_active"),
            },
        )
