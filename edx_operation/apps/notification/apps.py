from django.apps import AppConfig


class NotificationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "edx_operation.apps.notification"

    def ready(self) -> None:
        import edx_operation.apps.notification.signals
