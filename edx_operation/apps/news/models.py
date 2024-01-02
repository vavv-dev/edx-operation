from edx_operation.apps.wagtail_common.models import AbstractPostHome, AbstractPostPage


class NewsHome(AbstractPostHome):
    class Meta:
        verbose_name = "뉴스"
        verbose_name_plural = verbose_name

    subpage_types = ["NewsPage"]
    template = "wagtail_common/post_home.html"


class NewsPage(AbstractPostPage):
    class Meta:
        verbose_name = "뉴스"
        verbose_name_plural = verbose_name

    parent_page_types = ["NewsHome"]
    subpage_types = []
    template = "wagtail_common/post_page.html"

