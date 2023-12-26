from django.dispatch import receiver

from edx_operation.apps.event_bus.service import OPERATION_EVENT_SIGNAL

from .models import Enrollment


@receiver(OPERATION_EVENT_SIGNAL)
def courseenrollment(event, **kwargs):
    """courseenrollment.

    :param event:
        {
            "timestamp": 1703163178.0,
            "event_type": "operation_event.signals.courseenrollment",
            "message": {
                "created": "2023-12-20 21:48:01.117592+00:00",
                "id": 53,
                "username": "edx",
                "course_id": "course-v1:인공지능+lyadtrfx+preview",
                "mode": "audit",
                "is_active": false
            },
            "created": false,
            "deleted": false,
            "time": "2023-12-21 12:52:57.896100+00:00",
            "request_username": "edx",
            "client_ip": "192.168.65.1",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "source": "stdout",
            "container_id": "45a40806caba60e7fb68892b9694c1a67f725ff4ce713f90505d947b95116ac2",
            "container_name": "/edx.devstack.lms"
        }
    :param kwargs:
    """

    if event.event_type != "operation_event.signals.courseenrollment":
        return

    m = event.message

    Enrollment.objects.update_or_create(
        courserun_id=m.get("course_id"),
        student_id=m.get("username"),
        defaults={
            "created": m.get("created"),
            "courserun_id": m.get("course_id"),
            "student_id": m.get("username"),
            "mode": m.get("mode"),
            "is_active": m.get("is_active"),
        },
    )
