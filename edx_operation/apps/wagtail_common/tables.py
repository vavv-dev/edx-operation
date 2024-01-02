from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.html import format_html, escape
from django_tables2 import Column
from wagtail.models import Page

from edx_operation.apps.core.tables import SelectTableMixin


class PageTable(SelectTableMixin):
    class Meta(SelectTableMixin.Meta):
        model = Page

    priority = Column(verbose_name="")
    title = Column(verbose_name="제목")
    last_published_at = Column(verbose_name="수정")
    rating_count = Column(verbose_name="추천")
    hit_count = Column(verbose_name="조회")

    def render_priority(self, value, record):
        return format_html('<i class="bi bi-pin-angle"></i>') if value else ""

    def render_title(self, value, record):
        value = escape(value)
        if record.comment_count:
            value += f" <span>({record.comment_count})</span>"
        return format_html(f'<a href="{record.url}">{value}</a>')

    def render_last_published_at(self, value, record):
        return naturaltime(record.last_published_at)
