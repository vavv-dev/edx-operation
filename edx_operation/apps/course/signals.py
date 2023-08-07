from django.dispatch import receiver
from opaque_keys.edx.keys import CourseKey
from edx_operation.apps.course.models import Course, CourseAccessRole

from edx_operation.apps.event.kafka import OPERATION_EVENT_SIGNAL


@receiver(OPERATION_EVENT_SIGNAL)
def receive_edx_tracking_log(event, **kwargs):
    if event.event_type == "operation_event.signals.courseoverview":
        m = event.message

        course_id = CourseKey.from_string(m.get("id"))
        course, __ = Course.objects.update_or_create(
            id=course_id,
            defaults={
                "org": course_id.org,
                "number": course_id.course,
                "run": course_id.run,
                "created": m.get("created"),
                "modified": m.get("modified"),
                "display_name": m.get("display_name"),
                "invitation_only": m.get("invitation_only"),
                "course_image_url": m.get("course_image_url"),
                "effort": m.get("effort"),
                "visible_to_staff_only": m.get("visible_to_staff_only"),
                "start": m.get("start"),
                "end": m.get("end"),
                "enrollment_start": m.get("enrollment_start"),
                "enrollment_end": m.get("enrollment_end"),
                "certificate_available_date": m.get("certificate_available_date"),
                "pacing": m.get("pacing"),
            },
        )

        if event.created:
            course.create_course_modes()

    elif event.event_type == "operation_event.signals.courseaccessrole":
        m = event.message

        CourseAccessRole.objects.update_or_create(
            id=m.get("id"),
            defaults={
                "student_id": m.get("user_id"),
                "course_id": m.get("course_id"),
                "org": m.get("org"),
                "role": m.get("role"),
                "deleted": event.deleted,
            },
        )
