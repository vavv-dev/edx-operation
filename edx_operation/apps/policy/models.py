from django.db.models import BooleanField, CharField
from wagtail.admin.panels import FieldPanel
from edx_operation.apps.wagtail_common.models import AbstractPostHome, AbstractPostPage


class PolicyHome(AbstractPostHome):
    class Meta:
        verbose_name = "이용 규정"
        verbose_name_plural = verbose_name

    subpage_types = ["PolicyPage"]
    template = "wagtail_common/post_home.html"


class PolicyPage(AbstractPostPage):
    class Meta:
        verbose_name = "이용 규정"
        verbose_name_plural = verbose_name

    parent_page_types = ["PolicyHome"]
    subpage_types = []
    template = "wagtail_common/post_page.html"

    version = CharField("버전", max_length=10, default="1.0.0")
    mandatory = BooleanField("동의 필수 사항", default=True)

    content_panels = AbstractPostPage.content_panels + [
        FieldPanel("version"),
        FieldPanel("mandatory"),
    ]
