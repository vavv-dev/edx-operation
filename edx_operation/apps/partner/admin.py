from django.apps import apps
from django.contrib import admin

current_app_label = __package__.rsplit(".", 1)[-1]
app_models = apps.get_app_config(current_app_label).get_models()

for model in app_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
