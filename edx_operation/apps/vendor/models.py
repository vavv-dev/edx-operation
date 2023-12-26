from django.db.models import BooleanField, CharField, ForeignKey, SET_NULL, URLField
from django_extensions.db.models import TimeStampedModel
from taggit.managers import TaggableManager
from wagtail.admin.panels import FieldPanel
from wagtail.models import ClusterableModel
from wagtail.search.index import AutocompleteField, Indexed, SearchField
from wagtail.snippets.models import register_snippet

from edx_operation.apps.wagtail_common.models import Tagging


@register_snippet
class VendorBanner(TimeStampedModel, ClusterableModel, Indexed):
    class Meta:
        verbose_name = "벤터 배너"
        verbose_name_plural = verbose_name

    is_active = BooleanField("활성", default=False)
    url = URLField("링크 URL", max_length=254)
    title = CharField("제목", max_length=254, db_index=True)
    image = ForeignKey("wagtailimages.Image", on_delete=SET_NULL, null=True, related_name="+")
    vendor_contact = CharField("벤터 담당자 연락처", null=True, blank=True)
    tags = TaggableManager("태그", through=Tagging, blank=True)

    search_fields = (
        SearchField("title"),
        AutocompleteField("title"),
    )

    panels = [
        FieldPanel("is_active"),
        FieldPanel("url"),
        FieldPanel("title"),
        FieldPanel("image"),
        FieldPanel("vendor_contact"),
    ]

    def __str__(self):
        return self.title
