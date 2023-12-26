from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    ForeignKey,
    SmallIntegerField,
)
from django_extensions.db.models import TimeStampedModel
from taggit.managers import TaggableManager
from wagtail.admin.panels import FieldPanel
from wagtail.models import ClusterableModel
from wagtail.search.index import AutocompleteField, Indexed, SearchField
from wagtail.snippets.models import register_snippet

from edx_operation.apps.student.models import Student
from edx_operation.apps.wagtail_common.models import Tagging
from edx_operation.apps.wagtail_common.utils import StreamFieldFactory


@register_snippet
class Policy(TimeStampedModel, ClusterableModel, Indexed):
    class Meta:
        verbose_name = "이용 규정"
        verbose_name_plural = verbose_name
        unique_together = (("title", "version"),)
        ordering = ("ordering",)

    is_active = BooleanField("활성", default=False)
    title = CharField("제목", max_length=254, db_index=True)
    content = StreamFieldFactory("내용")
    version = CharField("버전", max_length=10, default="1.0.0")
    mandatory = BooleanField("동의 필수 사항", default=True, db_index=True)
    ordering = SmallIntegerField("화면 정렬 순서", default=1, db_index=True)
    tags = TaggableManager("태그", through=Tagging, blank=True)

    search_fields = (
        SearchField("title"),
        AutocompleteField("title"),
    )

    panels = [
        FieldPanel("is_active"),
        FieldPanel("title"),
        FieldPanel("content"),
        FieldPanel("version"),
        FieldPanel("mandatory"),
        FieldPanel("ordering"),
        FieldPanel("tags"),
    ]

    def __str__(self):
        return self.title


class PolicyConsent(TimeStampedModel):
    class Meta:
        verbose_name = "이용 규정 동의"
        verbose_name_plural = verbose_name

    student = ForeignKey(Student, on_delete=CASCADE, verbose_name="학습자")
    policy = ForeignKey(Policy, on_delete=CASCADE, verbose_name="이용 규정")
    has_consented = BooleanField("동의", default=True)

    panels = [
        FieldPanel("student"),
        FieldPanel("policy"),
        FieldPanel("has_consented"),
    ]
