from django.apps import AppConfig


class EventConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "edx_operation.apps.event_bus"
    verbose_name = "이벤트 시스템"
