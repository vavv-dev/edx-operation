from django.apps import AppConfig


class PartnerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "edx_operation.apps.partner"

    def ready(self) -> None:
        import edx_operation.apps.partner.signals
