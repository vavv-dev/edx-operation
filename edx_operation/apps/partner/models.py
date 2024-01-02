from django.db.models import ForeignKey, SET_NULL
from wagtail.admin.panels import FieldPanel

from edx_operation.apps.wagtail_common.models import AbstractPostHome, AbstractPostPage


class PartnerHome(AbstractPostHome):
    class Meta:
        verbose_name = "파트너"
        verbose_name_plural = verbose_name

    subpage_types = ["PartnerPage"]
    template = "wagtail_common/post_home.html"


class PartnerPage(AbstractPostPage):
    class Meta:
        verbose_name = "파트너"
        verbose_name_plural = verbose_name

    parent_page_types = ["PartnerHome"]
    subpage_types = []
    template = "wagtail_common/post_page.html"

    logo = ForeignKey("wagtailimages.Image", on_delete=SET_NULL, null=True, related_name="+")

    content_panels = AbstractPostPage.content_panels + [
        FieldPanel("logo"),
    ]
