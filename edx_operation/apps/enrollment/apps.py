from django.apps import AppConfig


class EnrollmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "edx_operation.apps.enrollment"
    verbose_name = "수강"

    def ready(self):
        from . import signals
