from wagtail.admin.panels import FieldPanel


class ReadOnlyLinkPanel(FieldPanel):
    read_only_output_template_name = "wagtailadmin/panels/read_only_output_link.html"

    def format_value_for_display(self, value):
        if callable(getattr(value, "all", "")):
            return [(str(obj), obj.url) for obj in value.all()] or "None"

        return super().format_value_for_display(value)
