from django.apps import AppConfig


class ForumConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "edx_operation.apps.forum"

    def ready(self) -> None:
        import edx_operation.apps.forum.signals
