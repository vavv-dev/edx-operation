import os
from pathlib import Path

from django.apps import apps
from django.forms import ChoiceField
from wagtail.admin.panels import WagtailAdminPageForm


class ThemeSelectAdminPageForm(WagtailAdminPageForm):
    theme = ChoiceField(choices=(), required=True, label="사이트 테마")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set theme choices
        app_label = self.instance._meta.app_label
        theme_dir = Path(apps.get_app_config(app_label).path) / f"templates/{app_label}/themes/"

        try:
            theme_names = [(dirname, dirname) for dirname in os.listdir(theme_dir)]
        except FileNotFoundError:
            theme_names = []

        theme_names.insert(0, ("default", "default"))
        self.fields["theme"].choices = theme_names
