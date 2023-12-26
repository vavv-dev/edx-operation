from django.db.models import (
    BooleanField,
    CASCADE,
    ForeignKey,
    ManyToManyField,
    SET_NULL,
    SmallIntegerField,
)
from django.db.models.fields import PositiveBigIntegerField
from taggit.managers import TaggableManager
from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel
from wagtail.admin.panels import MultipleChooserPanel
from wagtail.fields import StreamField
from wagtail.models import ClusterableModel, Orderable, ParentalKey
from wagtail.query import CharField
from wagtail.search.index import AutocompleteField, Indexed, SearchField
from wagtail.snippets.models import register_snippet

from edx_operation.apps.core.utils.common import secure_redeem_code
from edx_operation.apps.course.models import Course
from edx_operation.apps.wagtail_common.models import Category, Tagging
from edx_operation.apps.wagtail_common.utils import StreamFieldFactory

from .blocks import TextbookBlock, TuitionAssistanceBlock, TutorBlock


@register_snippet
class LmsCourse(Indexed, Course):
    class Meta:
        proxy = True
        verbose_name = "과정"
        verbose_name_plural = verbose_name

    search_fields = [
        SearchField("display_name"),
        AutocompleteField("display_name"),
    ]


class ProductLmsCourse(Orderable):
    product = ParentalKey("CourseProduct", on_delete=CASCADE, related_name="courses")
    course = ForeignKey(LmsCourse, on_delete=CASCADE, related_name="+")


class RelatedCourseProduct(Orderable):
    product = ParentalKey("CourseProduct", on_delete=CASCADE, related_name="related")
    related = ForeignKey("CourseProduct", on_delete=CASCADE, related_name="+")


@register_snippet
class CourseProduct(Indexed, ClusterableModel):
    class Meta:
        verbose_name = "과정 상품"
        verbose_name_plural = verbose_name

    # fmt: off

    title = CharField("제목", unique=True)
    is_active = BooleanField("활성", default=True)
    sku = CharField("상품 코드", default=secure_redeem_code, unique=True)
    cover = ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=SET_NULL, related_name="+")
    description = StreamFieldFactory("상품 소개")
    enrollment_days = SmallIntegerField("수강 일 수", default=0)
    price = PositiveBigIntegerField("가격", default=0)
    tuition_assistances = StreamField(
        [("tuition_assistance", TuitionAssistanceBlock())],
        null=True,
        blank=True,
        verbose_name="교육비 지원",
        use_json_field=True,
    )
    tutor = StreamField(
        [("tutor", TutorBlock())],
        null=True,
        blank=True,
        verbose_name="교강사",
        use_json_field=True,
    )
    textbook = StreamField(
        [("textbook", TextbookBlock())],
        null=True,
        blank=True,
        verbose_name="교재",
        use_json_field=True,
    )
    categories = ManyToManyField(Category, blank=True, verbose_name="카테고리")
    tags = TaggableManager(through=Tagging, blank=True, verbose_name="태그")

    # fmt: on

    # search

    search_fields = [
        SearchField("title"),
        AutocompleteField("title"),
    ]

    # panels

    panels = [
        FieldPanel("title"),
        MultiFieldPanel(
            [
                HelpPanel(
                    "두 개 이상 과정이 선택되면 단품 상품이 아닌 컬렉션으로 구분됩니다. <br/>"
                    "컬렉션은 즉시 과정에 등록되지 않고 선택한 과정에 등록할 권한이 부여됩니다."
                ),
                MultipleChooserPanel("courses", "course"),
            ],
            heading="과정 선택",
        ),
        FieldPanel("is_active"),
        FieldPanel("sku"),
        FieldPanel("cover"),
        FieldPanel("description"),
        FieldPanel("enrollment_days"),
        FieldPanel("price"),
        FieldPanel("tuition_assistances"),
        FieldPanel("tutor"),
        FieldPanel("textbook"),
        FieldPanel("categories"),
        FieldPanel("tags"),
        MultipleChooserPanel("related", "related", label="관련 과정"),
    ]

    # fmt: on
