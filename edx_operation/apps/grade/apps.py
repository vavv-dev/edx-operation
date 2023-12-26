from django.apps import AppConfig


class GradeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "edx_operation.apps.grade"
    verbose_name = "성적"

    def ready(self) -> None:
        from . import signals
