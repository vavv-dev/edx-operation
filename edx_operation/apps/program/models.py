from django.db.models import CASCADE, ForeignKey, SET_NULL, SmallIntegerField
from django.db.models.fields import PositiveBigIntegerField
from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel
from wagtail.admin.panels import MultipleChooserPanel
from wagtail.fields import StreamField
from wagtail.models import Orderable, ParentalKey
from wagtail.query import CharField
from wagtail.search.index import AutocompleteField, Indexed, SearchField
from wagtail.snippets.models import register_snippet

from edx_operation.apps.core.utils.common import secure_redeem_code
from edx_operation.apps.course.models import Course as BaseCourse
from edx_operation.apps.wagtail_common.models import AbstractPostHome, AbstractPostPage

from .blocks import TextbookBlock, TuitionAssistanceBlock, TutorBlock


class ProgramHome(AbstractPostHome):
    class Meta:
        verbose_name = "프로그램"
        verbose_name_plural = verbose_name

    subpage_types = ["ProgramPage"]
    template = "wagtail_common/post_home.html"


class ProgramPage(AbstractPostPage):
    class Meta:
        verbose_name = "프로그램"
        verbose_name_plural = verbose_name

    parent_page_types = ["ProgramHome"]
    subpage_types = []
    template = "wagtail_common/post_page.html"

    # fmt: off

    sku = CharField("프로그램 코드", default=secure_redeem_code, unique=True)
    cover = ForeignKey("wagtailimages.Image", null=True, on_delete=SET_NULL, related_name="+")
    enrollment_days = SmallIntegerField("수강 기간", default=0)
    price = PositiveBigIntegerField("가격", default=0)

    tuition_assistances = StreamField(
        [("tuition_assistance", TuitionAssistanceBlock())],
        null=True,
        blank=True,
        verbose_name="교육비 지원",
        use_json_field=True
    )
    tutor = StreamField(
        [("tutor", TutorBlock())],
        null=True,
        blank=True,
        verbose_name="교강사",
        use_json_field=True
    )
    textbook = StreamField(
        [("textbook", TextbookBlock())],
        null=True,
        blank=True,
        verbose_name="교재",
        use_json_field=True,
    )

    # fmt: on

    content_panels = AbstractPostPage.content_panels + [
        MultiFieldPanel(
            [
                HelpPanel(
                    "두 개 이상 과정으로 구성된 프로그램은 컬렉션이 됩니다.<br/>"
                    "컬렉션은 즉시 과정에 등록되지 않고 선택한 과정에 등록할 권한이 부여됩니다."
                ),
                MultipleChooserPanel("courses", "course"),
            ],
            heading="과정 선택",
        ),
        FieldPanel("sku"),
        FieldPanel("cover"),
        FieldPanel("enrollment_days"),
        FieldPanel("price"),
        FieldPanel("tuition_assistances"),
        FieldPanel("tutor"),
        FieldPanel("textbook"),
        MultipleChooserPanel("related_programs", "related_program", label="관련 과정"),
    ]


@register_snippet
class Course(Indexed, BaseCourse):
    class Meta:
        proxy = True
        verbose_name = "과정"
        verbose_name_plural = verbose_name

    search_fields = [
        SearchField("display_name"),
        AutocompleteField("display_name"),
    ]


class ProgramCourse(Orderable):
    program = ParentalKey(ProgramPage, on_delete=CASCADE, related_name="courses")
    course = ForeignKey(Course, on_delete=CASCADE, related_name="+")


class ProgramProgram(Orderable):
    program = ParentalKey(ProgramPage, on_delete=CASCADE, related_name="related_programs")
    related_program = ForeignKey(ProgramPage, on_delete=CASCADE, related_name="+")
