from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RawHTMLBlock, RichTextBlock, StreamBlock
from wagtail.fields import StreamField
from wagtail.models import Page

from .blocks import BannerBlock, TaggedContentBlock


class Portal(Page):
    class Meta:
        verbose_name = "포털"
        verbose_name_plural = verbose_name

    blocks = StreamField(
        [
            # banner
            (
                "banner",
                StreamBlock(
                    [("banner", BannerBlock(label="배너", required=False))],
                    heading="배너",
                    collapsed=True,
                ),
            ),
            # editor
            ("richtext", RichTextBlock(label="에디터", required=False)),
            ("html", RawHTMLBlock(label="HTML 코드", required=False)),
            # content blocks
            ("notice", TaggedContentBlock("noticepage", label="알림")),
            ("news", TaggedContentBlock("newspage", label="뉴스")),
            ("blog", TaggedContentBlock("blogpage", label="블로그")),
            ("popup", TaggedContentBlock("popuppage", label="팝업")),
            ("policy", TaggedContentBlock("policypage", label="이용 규정")),
            ("partner", TaggedContentBlock("partnerpage", label="파트너")),
            ("program", TaggedContentBlock("programpage", label="프로그램")),
            ("survey", TaggedContentBlock("surveypage", label="설문조사")),
            ("catalog", TaggedContentBlock("catalogpage", label="카탈로그")),
        ],
        null=True,
        blank=True,
        verbose_name="블록",
        use_json_field=True,
    )

    footer = StreamField(
        [
            ("richtext", RichTextBlock(label="에디터", required=False)),
            ("html", RawHTMLBlock(label="HTML 코드", required=False)),
        ],
        null=True,
        blank=True,
        verbose_name="푸터",
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("blocks"),
        FieldPanel("footer"),
    ]
