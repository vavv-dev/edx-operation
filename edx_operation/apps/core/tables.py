from itertools import count

from django.utils.html import format_html
from django_tables2 import CheckBoxColumn, Column, Table


class SelectTableMixin(Table):
    """TableMixin.

    select checkbox column, counter column 추가
    """

    class Meta:
        """Meta."""

        template_name = "django_tables2/bootstrap5.html"
        fields = ()
        default = ""
        attrs = {
            "class": "table",
            "tbody": {"class": "table-group-divider"},
        }
        per_page = 25

    selection = CheckBoxColumn(
        verbose_name="",
        empty_values=(),
        orderable=False,
        exclude_from_export=True,
    )
    counter = Column(
        verbose_name=format_html('<a href=".">NO.</a>'),  # reset sorting
        empty_values=(),
        orderable=False,
        exclude_from_export=True,
    )

    def render_selection(self, value, record):
        """render_selection.

        :param value:
        :param record:
        """
        return format_html(
            f'<input type="checkbox" class="form-check-input" name="selection" value="{record.id}"/>'
        )

    def render_counter(self, value, record):
        """value_counter.

        :param value:
        :param record:
        """
        if not hasattr(self, "page"):
            self.row_counter = getattr(self, "row_counter", count())
            counter = next(self.row_counter) + 1
        else:
            self.row_counter = getattr(self, "row_counter", count())
            counter = next(self.row_counter) + ((self.page.number - 1) * self.paginator.per_page)
            counter = self.page.paginator.count - (counter)

        return counter

    def __init__(self, *args, **kwargs):
        """__init__.

        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
