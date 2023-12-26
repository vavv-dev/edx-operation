from wagtail.snippets.models import register_snippet

from edx_operation.apps.wagtail_common.mixin import BasePostMixin


@register_snippet
class Notice(BasePostMixin):
    class Meta:
        verbose_name = "공지 사항"
        verbose_name_plural = verbose_name
