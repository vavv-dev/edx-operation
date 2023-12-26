from django.apps import AppConfig


class WagtailCommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "edx_operation.apps.wagtail_common"
    verbose_name = "웨그테일"

    def ready(self) -> None:
        from . import wagtail_hooks
