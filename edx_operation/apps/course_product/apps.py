from django.apps import AppConfig


class CourseProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "edx_operation.apps.course_product"
    verbose_name = "LMS 사이트"

    def ready(self) -> None:
        from . import views
