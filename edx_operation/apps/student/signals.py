from django.dispatch import receiver

from edx_operation.apps.event.kafka import OPERATION_EVENT_SIGNAL
from edx_operation.apps.student.models import Student


@receiver(OPERATION_EVENT_SIGNAL)
def log_operation_event(event, **kwargs):
    if event.event_type == "operation_event.signals.user":
        m = event.message
        Student.objects.update_or_create(
            id=m.get("id"),
            defaults={
                "username": m.get("username"),
                "email": m.get("email"),
                "is_active": m.get("is_active"),
                "is_staff": m.get("is_staff"),
                "is_superuser": m.get("is_superuser"),
                "last_login": m.get("last_login"),
                "date_joined": m.get("date_joined"),
            },
        )

    elif event.event_type == "operation_event.signals.userprofile":
        m = event.message
        Student.objects.update_or_create(
            id=m.get("user_id"),
            defaults={
                "name": m.get("name"),
                "year_of_birth": m.get("year_of_birth"),
            },
        )
