from django.apps import AppConfig


class CourseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "edx_operation.apps.course"
    verbose_name = "과정"

    def ready(self):
        from . import signals
