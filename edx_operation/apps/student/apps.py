from django.apps import AppConfig


class StudentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "edx_operation.apps.student"

    def ready(self) -> None:
        import edx_operation.apps.student.signals
