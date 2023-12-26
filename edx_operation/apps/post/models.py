from django.db.models import URLField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from edx_operation.apps.wagtail_common.mixin import BasePostMixin
from edx_operation.apps.wagtail_common.utils import StreamFieldFactory


@register_snippet
class Post(BasePostMixin):
    class Meta:
        verbose_name = "포스트"
        verbose_name_plural = verbose_name

    # override
    content = StreamFieldFactory("내용", null=True, blank=True)

    # addtional fields
    outlink = URLField("아웃링크 URL", max_length=254, null=True, blank=True)

    panels = (
        BasePostMixin.top_panels
        + [
            FieldPanel("outlink"),
        ]
        + BasePostMixin.bottom_panels
    )
