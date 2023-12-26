from django.apps import AppConfig


class OperationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "edx_operation.apps.operation"
    verbose_name = "운영"

    def ready(self) -> None:
        from . import signals
