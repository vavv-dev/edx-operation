from edx_operation.apps.wagtail_common.models import AbstractPostHome, AbstractPostPage


class IndustryHome(AbstractPostHome):
    class Meta:
        verbose_name = "교육 분야"
        verbose_name_plural = verbose_name

    subpage_types = ["IndustryPage"]
    template = "wagtail_common/post_home.html"


class IndustryPage(AbstractPostPage):
    class Meta:
        verbose_name = "교육 분야"
        verbose_name_plural = verbose_name

    parent_page_types = ["IndustryHome"]
    subpage_types = []
    template = "wagtail_common/post_page.html"
