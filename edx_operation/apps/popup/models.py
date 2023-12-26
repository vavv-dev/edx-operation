from colorfield.fields import ColorField
from django.db.models import DateTimeField
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet

from edx_operation.apps.wagtail_common.mixin import BasePostMixin


@register_snippet
class Popup(BasePostMixin):
    class Meta:
        verbose_name = "팝업"
        verbose_name_plural = verbose_name

    # addtional fields
    start = DateTimeField("게시 시작")
    end = DateTimeField("게시 종료")
    background_color = ColorField("배경색", default="#FAFAFA", format="hexa")

    panels = (
        BasePostMixin.top_panels
        + [
            MultiFieldPanel(
                [FieldRowPanel([FieldPanel("start"), FieldPanel("end")])],
                heading="게시 기간",
            ),
            FieldPanel("background_color"),
        ]
        + BasePostMixin.bottom_panels
    )
