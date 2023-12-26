from django.apps import AppConfig


class CustomerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "edx_operation.apps.customer"
    verbose_name = "고객사"
