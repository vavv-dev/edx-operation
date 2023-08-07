from django.apps import AppConfig


class CourseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "edx_operation.apps.course"

    def ready(self):
        import edx_operation.apps.course.signals
