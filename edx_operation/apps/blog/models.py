from edx_operation.apps.wagtail_common.models import AbstractPostHome, AbstractPostPage


class BlogHome(AbstractPostHome):
    class Meta:
        verbose_name = "블로그"
        verbose_name_plural = verbose_name

    subpage_types = ["BlogPage"]
    template = "wagtail_common/post_home.html"


class BlogPage(AbstractPostPage):
    class Meta:
        verbose_name = "블로그"
        verbose_name_plural = verbose_name

    parent_page_types = ["BlogHome"]
    subpage_types = []
    template = "wagtail_common/post_page.html"
