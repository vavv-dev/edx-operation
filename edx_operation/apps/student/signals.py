from django.dispatch import receiver

from edx_operation.apps.event_bus.service import OPERATION_EVENT_SIGNAL
from .models import Student


@receiver(OPERATION_EVENT_SIGNAL)
def user(event, **kwargs):
    """user.

    :param event:
        {
            "timestamp": 1703163021.0,
            "event_type": "operation_event.signals.user",
            "message": {
                "id": 3,
                "username": "edx",
                "email": "edx@example.com",
                "is_active": true,
                "is_staff": true,
                "is_superuser": true,
                "last_login": "2023-12-21 07:40:04.672296+00:00",
                "date_joined": "2023-02-21 14:19:07.911310+00:00"
            },
            "created": false,
            "deleted": false,
            "time": "2023-12-21 12:50:21.037272+00:00",
            "request_username": "edx",
            "client_ip": "192.168.65.1",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "source": "stdout",
            "container_id": "45a40806caba60e7fb68892b9694c1a67f725ff4ce713f90505d947b95116ac2",
            "container_name": "/edx.devstack.lms"
        }
    :param kwargs:
    """

    if event.event_type != "operation_event.signals.user":
        return

    m = event.message
    Student.objects.update_or_create(
        id=m.get("username"),
        defaults={
            "email": m.get("email"),
            "is_active": m.get("is_active"),
            "is_staff": m.get("is_staff"),
            "is_superuser": m.get("is_superuser"),
            "last_login": m.get("last_login"),
            "date_joined": m.get("date_joined"),
        },
    )


@receiver(OPERATION_EVENT_SIGNAL)
def profile(event, **kwargs):
    """profile.

    :param event:
        {
            "timestamp": 1703163021.0,
            "event_type": "operation_event.signals.userprofile",
            "message": {
                "id": 1,
                "username": "edx",
                "name": "edx",
                "year_of_birth": null,
                "gender": null
            },
            "created": false,
            "deleted": false,
            "time": "2023-12-21 12:50:21.049244+00:00",
            "request_username": "edx",
            "client_ip": "192.168.65.1",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "source": "stdout",
            "container_id": "45a40806caba60e7fb68892b9694c1a67f725ff4ce713f90505d947b95116ac2",
            "container_name": "/edx.devstack.lms"
        }
    :param kwargs:
    """

    if event.event_type != "operation_event.signals.userprofile":
        return

    m = event.message
    Student.objects.update_or_create(
        id=m.get("username"),
        defaults={
            "name": m.get("name"),
            "year_of_birth": m.get("year_of_birth"),
            "gender": m.get("gender"),
        },
    )
