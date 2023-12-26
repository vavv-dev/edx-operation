from django.db.models import Max
from django.dispatch import receiver
from opaque_keys.edx.keys import CourseKey

from edx_operation.apps.core.constants import EMPTY_COURSE_DISPLAY_NAME as EMPTY
from edx_operation.apps.course.models import Course, CourseRun
from edx_operation.apps.event_bus.service import OPERATION_EVENT_SIGNAL


@receiver(OPERATION_EVENT_SIGNAL)
def courseoverview(event, **kwargs):
    """receive_operation_event.

    :param event:
        {
            "timestamp": 1703162866.0,
            "event_type": "operation_event.signals.courseoverview",
            "message": {
                "created": "2023-12-19 08:29:35.438387+00:00",
                "modified": "2023-12-21 12:47:44.011139+00:00",
                "id": "course-v1:병원+ohgpqtyg+20231219AG",
                "display_name": "인공지능시대의 스마트한 사무행정",
                "invitation_only": true,
                "course_image_url": "/asset-v1:병원+ohgpqtyg+20231219AG+type@asset+block@cover.png",
                "effort": "31H",
                "visible_to_staff_only": false,
                "start": "2023-12-18 15:00:00+00:00",
                "end": "2049-12-31 14:59:59+00:00",
                "enrollment_start": null,
                "enrollment_end": null,
                "certificate_available_date": "2049-12-31 14:59:59+00:00",
                "pacing": "instructor"
            },
            "created": false,
            "deleted": false,
            "time": "2023-12-21 21:47:44.048407+09:00",
            "request_username": "edx",
            "client_ip": "192.168.65.1",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "source": "stdout",
            "container_id": "076d3293b4a1b1ad2211e26eef40f2097b91cd68a9631ea5e42bd13462600719",
            "container_name": "/edx.devstack.cms"
        }
    :param kwargs:
    """

    if event.event_type != "operation_event.signals.courseoverview":
        return

    m = event.message
    courserun_id = CourseKey.from_string(m.get("id"))

    # create or update Course
    defaults = {
        "display_name": m.get("display_name"),
        "is_active": True,
        "effort": m.get("effort"),
    }

    course, course_created = Course.objects.get_or_create(
        id=courserun_id.course,
        defaults=defaults,
    )

    course_is_empty = course.display_name == EMPTY
    if not course_created and course_is_empty:
        for k, v in defaults.items():
            setattr(course, k, v)
        course.save()

    # create or update CourseRun
    defaults = {
        "course": course,
        "display_name": m.get("display_name"),
        "invitation_only": m.get("invitation_only"),
        "visible_to_staff_only": m.get("visible_to_staff_only"),
        "start": m.get("start"),
        "end": m.get("end"),
        "enrollment_start": m.get("enrollment_start"),
        "enrollment_end": m.get("enrollment_end"),
        "certificate_available_date": m.get("certificate_available_date"),
        "pacing": m.get("pacing"),
    }

    courserun, courserun_created = CourseRun.objects.get_or_create(
        id=courserun_id,
        defaults=defaults,
    )

    if courserun_created:
        courserun.run_number = course.next_course_run_number()
        courserun.save()
        courserun.sync_courserun_blocks()

    elif courserun.display_name == EMPTY:
        for k, v in defaults.items():
            setattr(courserun, k, v)
        courserun.save()
        courserun.sync_courserun_blocks()

    # update course contents
    if course_created or course_is_empty:
        course.update_grading(courserun)
        course.update_contents(courserun)
