from edx_operation.apps.wagtail_common.models import AbstractPostHome, AbstractPostPage


class NoticeHome(AbstractPostHome):
    class Meta:
        verbose_name = "알림"
        verbose_name_plural = verbose_name

    subpage_types = ["NoticePage"]
    template = "wagtail_common/post_home.html"


class NoticePage(AbstractPostPage):
    class Meta:
        verbose_name = "알림"
        verbose_name_plural = verbose_name

    parent_page_types = ["NoticeHome"]
    subpage_types = []
    template = "wagtail_common/post_page.html"
