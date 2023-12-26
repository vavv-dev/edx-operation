from django.apps import AppConfig


class StudentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "edx_operation.apps.student"
    verbose_name = "학습자"

    def ready(self) -> None:
        from . import signals
