from django.dispatch import receiver
from edx_operation.apps.forum.models import Post

from edx_operation.apps.event.kafka import OPERATION_EVENT_SIGNAL


@receiver(OPERATION_EVENT_SIGNAL)
def log_operation_event(event, **kwargs):
    if event.event_type == "operation_event.signals.forumpost":
        m = event.message

        Post.objects.update_or_create(
            id=m.get("id"),
            defaults={
                "title": m.get("title"),
                "body": m.get("body"),
                "annoymous": m.get("annoymous"),
                "course_id": m.get("course_id"),
                "thread_id": m.get("thread_id"),
                "parent_id": m.get("parent_id"),
                "depth": m.get("depth"),
                "commentable_id": m.get("commentable_id"),
                "student_id": m.get("user_id"),
                "thread_type": m.get("thread_type"),
                "created_at": m.get("created_at"),
                "updated_at": m.get("updated_at"),
                "closed": m.get("closed"),
                "votes": m.get("votes"),
                "type": m.get("type"),
                "deleted": event.deleted,
            },
        )
