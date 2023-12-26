import logging

from django.core.files.base import ContentFile
from django.db.models import BooleanField, CharField, IntegerField, TextField
from django.forms.widgets import CheckboxSelectMultiple
from django.template.response import TemplateResponse
from django.test import RequestFactory
from django.utils.timezone import localtime
from django_ace import AceWidget
from django_extensions.db.models import TimeStampedModel
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel
from wagtail.blocks import RawHTMLBlock, RichTextBlock
from wagtail.documents import get_document_model
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import ClusterableModel, Page, Task, TaskState
from weasyprint import HTML
from edx_operation.apps.wagtail_common.forms import ThemeSelectAdminPageForm

from edx_operation.apps.core.utils.common import paginate
from edx_operation.apps.course.models import Course
from edx_operation.apps.wagtail_common.mixin import ThemeSelectPageMixin

from .blocks import (
    CatalogImagePageBlock,
    CatalogPageBackgroundBlock,
    CatalogPageLogoBlock,
)


Documents = get_document_model()

log = logging.getLogger(__name__)


class CatalogSite(Page):
    """
    카탈로그 사이트
    """

    class Meta:
        verbose_name = "카탈로그 사이트"
        verbose_name_plural = verbose_name

    template = "catalog/catalog_site.html"
    subpage_types = ["CatalogCreator"]
    max_count = 1

    content = StreamField(
        [
            ("image", ImageChooserBlock(label="이미지", required=False)),
            ("richtext", RichTextBlock(label="텍스트", required=False)),
            ("embed", EmbedBlock(label="임베드", required=False)),
            ("html", RawHTMLBlock(label="HTML", required=False)),
        ],
        use_json_field=True,
        verbose_name="콘텐츠",
        null=True,
        blank=True,
    )

    # panels
    content_panels = Page.content_panels + [FieldPanel("content")]

    def get_context(self, request, *args, **kwargs):
        catalogs = (
            self.get_children()
            .type(CatalogCreator)
            .filter(catalogcreator__is_public=True)
            .live()
            .distinct()
            .order_by("-id")
        )

        # pagination
        page = request.GET.get("page")
        per_page = request.GET.get("per_page")
        catalogs = paginate(catalogs, page, per_page or 30)

        # pdf url
        for catalog in catalogs:
            last = catalog.specific.files.last()
            if last and last.url:
                catalog.file_url = last.url

        context = super().get_context(request, *args, **kwargs)
        context["catalogs"] = catalogs
        return context


class ManyToManyLinkPanel(FieldPanel):
    read_only_output_template_name = "wagtailadmin/panels/read_only_output_link.html"

    def format_value_for_display(self, value):
        if callable(getattr(value, "all", "")):
            return [(str(obj), obj.url) for obj in value.all()] or "None"

        return super().format_value_for_display(value)


class CatalogCreator(ThemeSelectPageMixin, ClusterableModel, TimeStampedModel):
    """
    카탈로그
    """

    class Meta:
        verbose_name = "카탈로그"
        verbose_name_plural = verbose_name

    class ContentsPage:
        """목차 페이지"""

        def __init__(self, contents):
            self.page_contents = contents

    base_form_class = ThemeSelectAdminPageForm
    error_template = "survey/error.html"
    parent_page_types = ["CatalogSite"]
    subpage_types = []

    # fmt: off

    is_public = BooleanField("공개", default=False)
    dpi = IntegerField("pdf 해상도", default=300, choices=((150, "저화질"), (300, "일반 화질"), (600, "고화질")))
    image_page = StreamField(
        [("image_page", CatalogImagePageBlock())],
        null=True,
        blank=True,
        verbose_name="이미지 페이지 삽입",
        use_json_field=True,
    )
    page_logo = StreamField(
        [("catalog_page_logo", CatalogPageLogoBlock())],
        null=True,
        blank=True,
        verbose_name="페이지 로고",
        use_json_field=True,
    )
    page_background = StreamField(
        [("catalog_page_background", CatalogPageBackgroundBlock())],
        null=True,
        blank=True,
        verbose_name="페이지 배경",
        use_json_field=True,
    )
    attach_contents_page = BooleanField("목차 페이지 첨부", default=True)
    courses = ParentalManyToManyField(Course, related_name="+", verbose_name="과정")
    course_sort = CharField("과정 정렬", max_length=255, null=True, blank=True)
    exclude_tag_names = CharField("태그 숨기기", max_length=255, null=True, blank=True, help_text="표시하지 않을 태그를 쉼표로 분리해서 입력하세요. 태그 표시만 숨깁니다.")
    files = ParentalManyToManyField(Documents, verbose_name="카탈로그 파일", related_name="+", blank=True)
    css = TextField("CSS", null=True, blank=True)

    # fmt: on

    content_panels = Page.content_panels + [
        FieldPanel("is_public"),
        FieldPanel("dpi"),
        FieldPanel("theme", heading="테마"),
        FieldPanel("attach_contents_page"),
        FieldPanel("image_page"),
        FieldPanel("page_logo"),
        FieldPanel("page_background"),
        FieldPanel("exclude_tag_names"),
        MultiFieldPanel(
            [
                HelpPanel(
                    "아래 항목으로 정렬하십시요. 쉼표로 분리해서 여러 필드로 정렬할 수 있습니다.<br/>"
                    "- 기호를 붙이면 내림차순으로 정렬됩니다. ex) -display_name<br/>"
                ),
                FieldPanel("course_sort"),
                FieldPanel("courses", widget=CheckboxSelectMultiple),
            ],
            heading="과정 선택",
        ),
        # ManyToManyLinkPanel("files", read_only=True),
        FieldPanel("files", read_only=True),
        FieldPanel(
            "css",
            widget=AceWidget(mode="css", width="100%", toolbar=True),
            classname="collapsed",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # catalog pages
        catalog_pages = []

        # courses
        per_column = 16

        # sort
        courses = self.courses.filter(is_active=True)

        if self.course_sort:
            try:
                sorters = [f.strip() for f in self.course_sort.split(",") if f]
                courses = courses.order_by(*sorters)

                # wagtail FakeQuerySet에서 nulls_last가 작동하지 않음
                # ascending에서만 fix

                for field in sorters:
                    if field.startswith("-"):
                        continue

                    def nulls_last(x):
                        value = getattr(x, field, None)
                        return not value, value

                    courses = sorted(courses, key=nulls_last)

            except Exception as e:
                log.error(e, exc_info=True)

            # wagtail preview 모드에서 order_by가 작동하지 않음

        # courses transform
        for course in courses:
            contents = [f"<li>{c}</li>" for c in course.contents.split("\n")]
            size = "small" if (len(contents) - 1) // per_column + 1 > 2 else ""
            course.contents = f'<ol class="{size}">{"".join(contents)}</ol>'
            course.title = course.display_name
            catalog_pages.append(course)

        # image pages
        for image_page in self.image_page:
            block = image_page.value
            block["image"].title = block["title"]
            catalog_pages.insert(block["insert_to"] - 1, block["image"])

        # 목차
        if self.attach_contents_page:
            contents = []

            for i, catalog_page in enumerate(catalog_pages, start=1):
                # (page number, title)
                contents.append((catalog_page.title, i))

            per_page = 30
            contents_page_start = 0 if type(catalog_pages[0]) == Course else 1
            contents_pages = range(0, len(contents), per_page)
            contents_pages_len = len(contents_pages)

            for i, g in enumerate(contents_pages):
                page_contents = contents[g : g + per_page]

                # update page number
                for k, (title, j) in enumerate(page_contents):
                    if j <= contents_page_start:
                        continue
                    page_contents[k] = title, j + contents_pages_len

                # insert to catalog_pages
                catalog_pages.insert(contents_page_start + i, self.ContentsPage(page_contents))

        # page logo, page background
        for name, stream_field in [("logo", self.page_logo), ("background", self.page_background)]:
            for f in stream_field:
                apply_to_pages = f.value["apply_to_pages"]
                if apply_to_pages:
                    for i in range(len(catalog_pages)):
                        insert = False
                        if apply_to_pages == "all":
                            insert = True
                        elif apply_to_pages == "odd" and not i % 2:
                            insert = True
                        elif apply_to_pages == "even" and i % 2:
                            insert = True

                        if insert:
                            setattr(catalog_pages[i], name, f.value["image"])

                apply_to_specific_pages = f.value["apply_to_specific_pages"]
                if apply_to_specific_pages:
                    numbers = apply_to_specific_pages.split(",")
                    for number in numbers:
                        if number:
                            try:
                                setattr(catalog_pages[int(number) - 1], name, f.value["image"])
                            except Exception:
                                pass

        context["catalog_pages"] = catalog_pages

        return context

    def create_catalog(self, user):
        # fake request
        request_factory = RequestFactory()
        fake_request = request_factory.get("/")
        fake_request.user = user

        context = self.get_context(fake_request)
        template = self.get_template(fake_request)
        res = TemplateResponse(fake_request, template, context)
        res.render()

        # create pdf
        pdf_bytes = HTML(string=res.content.decode("utf-8")).write_pdf(
            optimize_images=True,
            jpeg_quality=95,
            dpi=self.dpi,
        )

        if not pdf_bytes:
            log.info("weasyprint create emtpy file...")
            return

        # versioning
        version = f'{localtime().strftime("%Y%m%d")}-{self.dpi}-{self.files.count() + 1}'

        # File
        title = f"{self.title}-{version}"
        file = Documents(title=title, uploaded_by_user_id=user.id)
        file.file.save(f"{title}.pdf", ContentFile(pdf_bytes), save=True)
        file.tags.add("카탈로그")

        # attach file to self
        self.files.add(file)

        # publish
        self.save_revision().publish()


class CatalogCreateTaskState(TaskState):
    """
    카탈로그 생성 작업 상태
    """

    class Meta:
        verbose_name = "카탈로그 생성 작업 상태"
        verbose_name_plural = verbose_name


class CatalogCreateTask(Task):
    """
    카탈로그 생성 작업
    """

    class Meta:
        verbose_name = "카탈로그 생성 작업"
        verbose_name_plural = verbose_name

    task_state_class = CatalogCreateTaskState

    def user_can_access_editor(self, obj, user):
        return user.is_staff or user.is_superuser

    def locked_for_user(self, obj, user):
        return not (user.is_staff or user.is_superuser)

    def get_actions(self, obj, user):
        if user.is_staff or user.is_superuser:
            return [
                ("approve", "카탈로그 생성", False),
            ]
        else:
            return []

    def on_action(self, task_state, user, action_name, **kwargs):
        if action_name == "approve":
            # create catalog
            creator = task_state.revision.as_object()
            creator.create_catalog(user)

            # TODO notification

        return super().on_action(task_state, user, action_name, **kwargs)
