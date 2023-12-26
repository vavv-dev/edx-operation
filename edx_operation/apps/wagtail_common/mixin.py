from django.db.models import BooleanField, CharField, ForeignKey, IntegerField, SET_NULL
from django_extensions.db.models import TimeStampedModel
from taggit.managers import TaggableManager
from wagtail.admin.panels import FieldPanel
from wagtail.models import ClusterableModel, Page
from wagtail.search.index import AutocompleteField, Indexed, SearchField

from edx_operation.apps.core.models import User
from .models import Tagging
from .utils import StreamFieldFactory


class ThemeSelectPageMixin(Page):
    class Meta:
        abstract = True

    theme = CharField("테마", max_length=255, default="default", null=True, blank=True)

    def theme_dir(self):
        return f"{self._meta.app_label}/themes/{self.theme}"

    def theme_template(self, template):
        return f"{self.theme_dir()}/{template}"

    def get_template(self, request, *args, **kwargs):
        template = super().get_template(request, *args, **kwargs)
        if not self.theme or self.theme == "default":
            return template
        return self.theme_template(template)


class BasePostMixin(TimeStampedModel, ClusterableModel, Indexed):
    class Meta:
        abstract = True

    is_active = BooleanField("활성", default=False)
    login_required = BooleanField("로그인 필요", default=False)
    title = CharField("제목", max_length=254, db_index=True)
    content = StreamFieldFactory("내용")
    tags = TaggableManager("태그", through=Tagging, blank=True)
    creator = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, verbose_name="작성자")
    counter = IntegerField("조회수", default=0)

    # search

    search_fields = (
        SearchField("title"),
        AutocompleteField("title"),
    )

    # panels

    top_panels = [
        FieldPanel("is_active"),
        FieldPanel("login_required"),
        FieldPanel("title"),
        FieldPanel("content"),
    ]

    bottom_panels = [
        FieldPanel("tags"),
        FieldPanel("creator", read_only=True),
        FieldPanel("counter", read_only=True),
    ]

    panels = top_panels + bottom_panels

    def __str__(self):
        return self.title
