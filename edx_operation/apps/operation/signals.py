from django.dispatch import receiver

from edx_operation.apps.event_bus.service import OPERATION_EVENT_SIGNAL

from .models import CourseRunAccessRole, Post


@receiver(OPERATION_EVENT_SIGNAL)
def courseaccessrole(event, **kwargs):
    """courseaccessrole.

    :param event:
        {
            "timestamp": 1703163217.0,
            "event_type": "operation_event.signals.courseaccessrole",
            "message": {
                "id": 59,
                "username": "edx",
                "course_id": "course-v1:인공지능+lyadtrfx+preview",
                "org": "인공지능",
                "role": "staff"
            },
            "created": true,
            "deleted": false,
            "time": "2023-12-21 12:53:37.724891+00:00",
            "request_username": "edx",
            "client_ip": "192.168.65.1",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "source": "stdout",
            "container_id": "45a40806caba60e7fb68892b9694c1a67f725ff4ce713f90505d947b95116ac2",
            "container_name": "/edx.devstack.lms"
        }
    :param kwargs:
    """

    if event.event_type != "operation_event.signals.courseaccessrole":
        return

    m = event.message

    unique = {
        "courserun_id": m.get("course_id"),
        "student_id": m.get("username"),
        "org": m.get("org"),
        "role": m.get("role"),
    }

    if not event.deleted:
        CourseRunAccessRole.objects.update_or_create(**unique)
    else:
        CourseRunAccessRole.objects.filter(**unique).delete()


@receiver(OPERATION_EVENT_SIGNAL)
def forumpost(event, **kwargs):
    """forumpost.

    :param event:
        {
            "timestamp": 1703182075.0,
            "event_type": "operation_event.signals.forumpost",
            "message": {
                "title": "adfadadfafsdf",
                "body": "# adfadfadsfasdfads",
                "anonymous": false,
                "anonymous_to_peers": false,
                "course_id": "course-v1:인공지능+lyadtrfx+preview",
                "commentable_id": "i4x-인공지능-lyadtrfx-course-preview",
                "user_id": "3",
                "thread_type": "discussion",
                "context": "course",
                "created_at": "2023-12-21T18:07:54Z",
                "updated_at": "2023-12-21T18:07:54Z",
                "at_position_list": [],
                "closed": false,
                "last_activity_at": "2023-12-21T18:07:54Z",
                "id": "65847efaceb0b10423fa6012",
                "username": "edx",
                "votes": {
                    "count": 0,
                    "up_count": 0,
                    "down_count": 0,
                    "point": 0
                },
                "abuse_flaggers": [],
                "tags": [],
                "type": "thread",
                "group_id": null,
                "pinned": false,
                "comments_count": 0,
                "read": true,
                "unread_comments_count": 0,
                "endorsed": false,
                "resp_total": 0
            },
            "created": true,
            "deleted": false,
            "time": "2023-12-21 18:07:55.324837+00:00",
            "request_username": "edx",
            "client_ip": "192.168.65.1",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "source": "stdout",
            "container_id": "45a40806caba60e7fb68892b9694c1a67f725ff4ce713f90505d947b95116ac2",
            "container_name": "/edx.devstack.lms"
        }
    :param kwargs:
    """

    if event.event_type != "operation_event.signals.forumpost":
        return

    m = event.message

    Post.objects.update_or_create(
        id=m.get("id"),
        defaults={
            "title": m.get("title"),
            "body": m.get("body"),
            "annoymous": m.get("annoymous"),
            "courserun_id": m.get("course_id"),
            "thread_id": m.get("thread_id"),
            "parent_id": m.get("parent_id"),
            "depth": m.get("depth"),
            "commentable_id": m.get("commentable_id"),
            "student_id": m.get("username"),
            "thread_type": m.get("thread_type"),
            "created_at": m.get("created_at"),
            "updated_at": m.get("updated_at"),
            "closed": m.get("closed"),
            "votes": m.get("votes"),
            "type": m.get("type"),
            "deleted": event.deleted,
        },
    )
