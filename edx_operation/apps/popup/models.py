from colorfield.fields import ColorField
from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel

from edx_operation.apps.wagtail_common.models import AbstractPostHome, AbstractPostPage


class PopupHome(AbstractPostHome):
    class Meta:
        verbose_name = "팝업"
        verbose_name_plural = verbose_name

    subpage_types = ["PopupPage"]
    template = "wagtail_common/post_home.html"


class PopupPage(AbstractPostPage):
    class Meta:
        verbose_name = "팝업"
        verbose_name_plural = verbose_name

    parent_page_types = ["PopupHome"]
    subpage_types = []
    template = "wagtail_common/post_page.html"

    background_color = ColorField("배경색", default="#FAFAFA", format="hexa")

    content_panels = AbstractPostPage.content_panels + [
        MultiFieldPanel(
            [
                HelpPanel("오른쪽 상단에 있는 info 버튼을 클릭한 후 팝업 종료 기간을 입력하세요."),
            ],
            heading="팝업 기간",
        ),
        FieldPanel("background_color"),
    ]

    def clean(self):
        # TODO 팝업 종료 기간 확인
        pass
