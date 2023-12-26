from django.dispatch import receiver

from edx_operation.apps.event_bus.service import OPERATION_EVENT_SIGNAL
from .models import CourseRunGrade, ExamStatus, Submission, SubsectionGrade


@receiver(OPERATION_EVENT_SIGNAL)
def coursegrade(event, **kwargs):
    """coursegrade.

    :param event:
        {
            "timestamp": 1703161971.0,
            "event_type": "operation_event.signals.coursegrade",
            "message": {
                "username": "edx",
                "course_id": "course-v1:인공지능+lyadtrfx+preview",
                "percent_grade": 0.31,
                "letter_grade": null,
                "passed": false,
                "grade_summary": {
                    "진도": {
                        "min_count": 30,
                        "weight": 0.0,
                        "percent": 0.0,
                        "weighted_percent": 0.0
                    },
                    "진행평가": {
                        "min_count": 1,
                        "weight": 0.1,
                        "percent": 0.5,
                        "weighted_percent": 0.05
                    },
                    "시험": {
                        "min_count": 1,
                        "weight": 0.6,
                        "percent": 0.04,
                        "weighted_percent": 0.024
                    },
                    "과제": {
                        "min_count": 1,
                        "weight": 0.3,
                        "percent": 0.8,
                        "weighted_percent": 0.24
                    }
                }
            },
            "created": null,
            "deleted": null,
            "time": "2023-12-21 12:32:51.898913+00:00",
            "request_username": "edx",
            "client_ip": "192.168.65.1",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "source": "stdout",
            "container_id": "45a40806caba60e7fb68892b9694c1a67f725ff4ce713f90505d947b95116ac2",
            "container_name": "/edx.devstack.lms"
        }
    :param kwargs:
    """

    if event.event_type != "operation_event.signals.coursegrade":
        return

    m = event.message
    CourseRunGrade.objects.update_or_create(
        student_id=m.get("username"),
        courserun_id=m.get("course_id"),
        defaults={
            "percent_grade": m.get("percent_grade"),
            "letter_grade": m.get("letter_grade"),
            "passed": m.get("passed"),
            "grade_summary": m.get("grade_summary"),
        },
    )


@receiver(OPERATION_EVENT_SIGNAL)
def subsectiongrade(event, **kwargs):
    """subsectiongrade.

    :param event:
        {
            "timestamp": 1703159503.0,
            "event_type": "operation_event.signals.subsectiongrade",
            "message": {
                "username": "edx",
                "course_id": "course-v1:인공지능+lyadtrfx+preview",
                "usage_key": "block-v1:인공지능+lyadtrfx+preview+type@sequential+block@11e2c0420efe4f239e6ec3eb90f717c9",
                "earned_all": 4.0,
                "possible_all": 100.0,
                "earned_graded": 4.0,
                "possible_graded": 100.0
            },
            "created": null,
            "deleted": null,
            "time": "2023-12-21 11:51:43.157294+00:00",
            "request_username": "edx",
            "client_ip": "192.168.65.1",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "source": "stdout",
            "container_id": "45a40806caba60e7fb68892b9694c1a67f725ff4ce713f90505d947b95116ac2",
            "container_name": "/edx.devstack.lms"
        }
    :param kwargs:
    """

    if event.event_type != "operation_event.signals.subsectiongrade":
        return

    m = event.message
    defaults = {
        "earned_all": m.get("earned_all"),
        "possible_all": m.get("possible_all"),
        "earned_graded": m.get("earned_graded"),
        "possible_graded": m.get("possible_graded"),
    }

    due = m.get("due")
    if due:
        defaults["due"] = due

    SubsectionGrade.objects.update_or_create(
        student_id=m.get("username"),
        subsection_id=m.get("usage_key"),
        defaults=defaults,
    )


@receiver(OPERATION_EVENT_SIGNAL)
def blockcompletion(event, **kwargs):
    """blockcompletion.

    :param event:
        {
            "timestamp": 1703159503.0,
            "event_type": "operation_event.signals.blockcompletion",
            "message": {
                "username": "edx",
                "context_key": "course-v1:인공지능+lyadtrfx+preview",
                "block_key": "block-v1:인공지능+lyadtrfx+preview+type@problem+block@9feb4c332c3447f4578b",
                "subsection_usage_key": "block-v1:인공지능+lyadtrfx+preview+type@sequential+block@11e2c0420efe4f239e6ec3eb90f717c9",
                "subsection_complete": false,
                "due": "2049-12-31 14:59:59+00:00"
            },
            "created": null,
            "deleted": null,
            "time": "2023-12-21 11:51:43.514736+00:00",
            "request_username": "edx",
            "client_ip": "192.168.65.1",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "source": "stdout",
            "container_id": "45a40806caba60e7fb68892b9694c1a67f725ff4ce713f90505d947b95116ac2",
            "container_name": "/edx.devstack.lms"
        }
    :param kwargs:
    """

    if event.event_type != "operation_event.signals.blockcompletion":
        return

    m = event.message
    defaults = {
        "complete": m.get("subsection_complete"),
        "completion_block": m.get("block_key"),
        "client_ip": event.client_ip,
    }

    due = m.get("due")
    if due:
        defaults["due"] = due

    SubsectionGrade.objects.update_or_create(
        student_id=m.get("username"),
        subsection_id=m.get("subsection_usage_key"),
        defaults=defaults,
    )


@receiver(OPERATION_EVENT_SIGNAL)
def proctoredexamstudentattempt(event, **kwargs):
    """proctoredexamstudentattempt.

    :param event:
        {
            "timestamp": 1703161062.0,
            "event_type": "operation_event.signals.proctoredexamstudentattempt",
            "message": {
                "created": "2023-12-21 12:17:42.323650+00:00",
                "modified": "2023-12-21 12:17:42.323650+00:00",
                "id": 1,
                "username": "edx",
                "status": "created",
                "proctored_exam": {
                    "course_id": "course-v1:인공지능+lyadtrfx+preview",
                    "content_id": "block-v1:인공지능+lyadtrfx+preview+type@sequential+block@11e2c0420efe4f239e6ec3eb90f717c9",
                    "is_active": true
                }
            },
            "created": true,
            "deleted": false,
            "time": "2023-12-21 12:17:42.349063+00:00",
            "request_username": "edx",
            "client_ip": "192.168.65.1",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "source": "stdout",
            "container_id": "45a40806caba60e7fb68892b9694c1a67f725ff4ce713f90505d947b95116ac2",
            "container_name": "/edx.devstack.lms"
        }
        ---
        {
            "timestamp": 1703161062.0,
            "event_type": "operation_event.signals.proctoredexamstudentattempt",
            "message": {
                "created": "2023-12-21 12:17:42.323650+00:00",
                "modified": "2023-12-21 12:17:42.415329+00:00",
                "id": 1,
                "username": "edx",
                "status": "started",
                "proctored_exam": {
                    "course_id": "course-v1:인공지능+lyadtrfx+preview",
                    "content_id": "block-v1:인공지능+lyadtrfx+preview+type@sequential+block@11e2c0420efe4f239e6ec3eb90f717c9",
                    "is_active": true
                }
            },
            "created": false,
            "deleted": false,
            "time": "2023-12-21 12:17:42.426451+00:00",
            "request_username": "edx",
            "client_ip": "192.168.65.1",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "source": "stdout",
            "container_id": "45a40806caba60e7fb68892b9694c1a67f725ff4ce713f90505d947b95116ac2",
            "container_name": "/edx.devstack.lms"
        }
        ---
        {
            "timestamp": 1703161176.0,
            "event_type": "operation_event.signals.proctoredexamstudentattempt",
            "message": {
                "created": "2023-12-21 12:17:42.323650+00:00",
                "modified": "2023-12-21 12:19:32.986845+00:00",
                "id": 1,
                "username": "edx",
                "status": "submitted",
                "proctored_exam": {
                    "course_id": "course-v1:인공지능+lyadtrfx+preview",
                    "content_id": "block-v1:인공지능+lyadtrfx+preview+type@sequential+block@11e2c0420efe4f239e6ec3eb90f717c9",
                    "is_active": true
                }
            },
            "created": false,
            "deleted": false,
            "time": "2023-12-21 12:19:34.444757+00:00",
            "request_username": "edx",
            "client_ip": "192.168.65.1",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "source": "stdout",
            "container_id": "45a40806caba60e7fb68892b9694c1a67f725ff4ce713f90505d947b95116ac2",
            "container_name": "/edx.devstack.lms"
        }
    :param kwargs:
    """

    if event.event_type != "operation_event.signals.proctoredexamstudentattempt":
        return

    m = event.message
    exam = m.get("proctored_exam")

    ExamStatus.objects.update_or_create(
        student_id=m.get("username"),
        subsection_id=exam.get("content_id"),
        defaults={
            "is_active": exam.get("is_active"),
            "status": m.get("status"),
            "deleted": event.deleted,
        },
    )


@receiver(OPERATION_EVENT_SIGNAL)
def submission(event, **kwargs):
    """submission.

    :param event:
        {
            "timestamp": 1703159594.0,
            "event_type": "operation_event.signals.submission",
            "message": {
                "id": 2,
                "uuid": "ee8885cf-7fdf-44c5-bf9e-d56716839457",
                "student_item": {
                    "student_id": "779462774823f49a247032d62bbf2f84",
                    "course_id": "course-v1:인공지능+lyadtrfx+preview",
                    "item_id": "block-v1:인공지능+lyadtrfx+preview+type@openassessment+block@76e06282851390dd26fb"
                },
                "attempt_number": 1,
                "submitted_at": "2023-12-21 11:28:26.298822+00:00",
                "created_at": "2023-12-21 11:28:26.298837+00:00",
                "answer": {
                    "parts": [
                        {
                            "text": "adfadfdfadadfaddfa"
                        }
                    ],
                    "file_keys": [],
                    "files_descriptions": [],
                    "files_names": [],
                    "files_sizes": []
                },
                "status": "D",
                "username": "edx"
            },
            "created": false,
            "deleted": null,
            "time": "2023-12-21 11:53:14.184556+00:00",
            "request_username": "edx",
            "client_ip": "192.168.65.1",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "source": "stdout",
            "container_id": "45a40806caba60e7fb68892b9694c1a67f725ff4ce713f90505d947b95116ac2",
            "container_name": "/edx.devstack.lms"
        }
    :param kwargs:
    """

    if event.event_type != "operation_event.signals.submission":
        return

    m = event.message
    student_item = m.get("student_item")

    Submission.objects.update_or_create(
        uuid=m.get("uuid"),
        defaults={
            "student_id": m.get("username"),
            "block_id": student_item.get("item_id"),
            "submitted_at": m.get("submitted_at"),
            "answer": m.get("answer"),
            "status": m.get("status"),
        },
    )


@receiver(OPERATION_EVENT_SIGNAL)
def score(event, **kwargs):
    """score.

    :param event:
        {
            "timestamp": 1703159593.0,
            "event_type": "operation_event.signals.score",
            "message": {
                "id": 4,
                "submission": {
                    "uuid": "ee8885cf-7fdf-44c5-bf9e-d56716839457"
                },
                "points_earned": 0,
                "points_possible": 10,
                "created_at": "2023-12-21 11:53:13.323547+00:00",
                "reset": false
            },
            "created": true,
            "deleted": false,
            "time": "2023-12-21 11:53:13.349353+00:00",
            "request_username": "edx",
            "client_ip": "192.168.65.1",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "source": "stdout",
            "container_id": "45a40806caba60e7fb68892b9694c1a67f725ff4ce713f90505d947b95116ac2",
            "container_name": "/edx.devstack.lms"
        }
        ---
        {
            "timestamp": 1703159593.0,
            "event_type": "operation_event.signals.score",
            "message": {
                "id": 5,
                "submission": {
                    "uuid": null
                },
                "points_earned": 0,
                "points_possible": 0,
                "created_at": "2023-12-21 11:53:13.363251+00:00",
                "reset": true
            },
            "created": true,
            "deleted": false,
            "time": "2023-12-21 11:53:13.381369+00:00",
            "request_username": "edx",
            "client_ip": "192.168.65.1",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "source": "stdout",
            "container_id": "45a40806caba60e7fb68892b9694c1a67f725ff4ce713f90505d947b95116ac2",
            "container_name": "/edx.devstack.lms"
        }
    :param kwargs:
    """

    if event.event_type != "operation_event.signals.score":
        return

    m = event.message
    uuid = m.get("submission").get("uuid")
    if not uuid:
        return

    Submission.objects.update_or_create(
        uuid=uuid,
        defaults={
            "points_earned": m.get("points_earned"),
            "points_possible": m.get("points_possible"),
            "scored_at": m.get("created_at"),
            "score_reset": m.get("reset"),
        },
    )
