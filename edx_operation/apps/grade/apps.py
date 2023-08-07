from django.apps import AppConfig


class GradeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "edx_operation.apps.grade"

    def ready(self) -> None:
        import edx_operation.apps.grade.signals
