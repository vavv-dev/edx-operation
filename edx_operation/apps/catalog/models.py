import logging

from django.core.files.base import ContentFile
from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    ForeignKey,
    IntegerField,
    TextField,
)
from django.forms.widgets import CheckboxSelectMultiple
from django.template.response import TemplateResponse
from django.test import RequestFactory
from django.utils.timezone import localtime
from django_ace import AceWidget
from django_extensions.db.models import TimeStampedModel
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import (
    FieldPanel,
    HelpPanel,
    MultiFieldPanel,
    MultipleChooserPanel,
)
from wagtail.blocks import RawHTMLBlock, RichTextBlock
from wagtail.documents import get_document_model
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from django.utils.html import format_html
from wagtail.models import (
    ClusterableModel,
    Orderable,
    Page,
    ParentalKey,
    Task,
    TaskState,
)
from weasyprint import HTML

from edx_operation.apps.core.utils.common import paginate
from edx_operation.apps.program.models import ProgramPage
from edx_operation.apps.wagtail_common.models import AbstractPostHome, AbstractPostPage
from edx_operation.apps.wagtail_common.panels import ReadOnlyLinkPanel

from .blocks import (
    CatalogImagePageBlock,
    CatalogPageBackgroundBlock,
    CatalogPageLogoBlock,
)


Documents = get_document_model()

log = logging.getLogger(__name__)


class CatalogHome(AbstractPostHome):
    class Meta:
        verbose_name = "카탈로그"
        verbose_name_plural = verbose_name

    subpage_types = ["CatalogPage"]
    template = "wagtail_common/post_home.html"


class CatalogProgram(Orderable):
    catalog = ParentalKey("CatalogPage", on_delete=CASCADE, related_name="programs")
    program = ForeignKey(ProgramPage, on_delete=CASCADE)


class CatalogPage(AbstractPostPage):
    class Meta:
        verbose_name = "카탈로그"
        verbose_name_plural = verbose_name

    class ContentsPage:
        """목차 페이지"""

        def __init__(self, contents):
            self.page_contents = contents

    parent_page_types = ["CatalogHome"]
    subpage_types = []
    template = "wagtail_common/post_page.html"

    # fmt: off

    dpi = IntegerField(
        "pdf 해상도",
        default=300,
        choices=((150, "저화질"), (300, "일반 화질"), (600, "고화질")),
    )
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
    attach_contents = BooleanField("목차 페이지 첨부", default=True)
    catalog_files = ParentalManyToManyField(
        Documents, verbose_name="카탈로그 파일", related_name="+", blank=True
    )
    css = TextField("CSS", null=True, blank=True)

    # fmt: on

    content_panels = AbstractPostPage.content_panels + [
        MultipleChooserPanel("programs", "program", label="프로그램"),
        FieldPanel("dpi"),
        FieldPanel("attach_contents"),
        FieldPanel("image_page"),
        FieldPanel("page_logo"),
        FieldPanel("page_background"),
        ReadOnlyLinkPanel("catalog_files", read_only=True),
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

        # contents
        per_column = 16

        programs = self.programs

        if not programs:
            return context

        # # programs transform
        # for program in programs:
        #     contents = [f"<li>{c}</li>" for c in program.contents.split("\n")]
        #     size = "small" if (len(contents) - 1) // per_column + 1 > 2 else ""
        #     course.contents = f'<ol class="{size}">{"".join(contents)}</ol>'
        #     course.title = course.display_name
        #     catalog_pages.append(course)

        # # image pages
        # for image_page in self.image_page:
        #     block = image_page.value
        #     block["image"].title = block["title"]
        #     catalog_pages.insert(block["insert_to"] - 1, block["image"])

        # # 목차
        # if self.attach_contents:
        #     contents = []

        #     for i, catalog_page in enumerate(catalog_pages, start=1):
        #         # (page number, title)
        #         contents.append((catalog_page.title, i))

        #     per_page = 30
        #     contents_page_start = 0 if type(catalog_pages[0]) == Course else 1
        #     contents_pages = range(0, len(contents), per_page)
        #     contents_pages_len = len(contents_pages)

        #     for i, g in enumerate(contents_pages):
        #         page_contents = contents[g : g + per_page]

        #         # update page number
        #         for k, (title, j) in enumerate(page_contents):
        #             if j <= contents_page_start:
        #                 continue
        #             page_contents[k] = title, j + contents_pages_len

        #         # insert to catalog_pages
        #         catalog_pages.insert(contents_page_start + i, self.ContentsPage(page_contents))

        # # page logo, page background
        # for name, stream_field in [("logo", self.page_logo), ("background", self.page_background)]:
        #     for f in stream_field:
        #         apply_to_pages = f.value["apply_to_pages"]
        #         if apply_to_pages:
        #             for i in range(len(catalog_pages)):
        #                 insert = False
        #                 if apply_to_pages == "all":
        #                     insert = True
        #                 elif apply_to_pages == "odd" and not i % 2:
        #                     insert = True
        #                 elif apply_to_pages == "even" and i % 2:
        #                     insert = True

        #                 if insert:
        #                     setattr(catalog_pages[i], name, f.value["image"])

        #         apply_to_specific_pages = f.value["apply_to_specific_pages"]
        #         if apply_to_specific_pages:
        #             numbers = apply_to_specific_pages.split(",")
        #             for number in numbers:
        #                 if number:
        #                     try:
        #                         setattr(catalog_pages[int(number) - 1], name, f.value["image"])
        #                     except Exception:
        #                         pass

        # context["catalog_pages"] = catalog_pages

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
        version = f'{localtime().strftime("%Y%m%d")}-{self.dpi}-{self.catalog_files.count() + 1}'

        # File
        title = f"{self.title}-{version}"
        file = Documents(title=title, uploaded_by_user_id=user.id)
        file.file.save(f"{title}.pdf", ContentFile(pdf_bytes), save=True)
        file.tags.add("카탈로그")

        # attach file to self
        self.catalog_files.add(file)

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
