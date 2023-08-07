from django.apps import AppConfig


class EnrollmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "edx_operation.apps.enrollment"

    def ready(self):
        import edx_operation.apps.enrollment.signals
