from colorfield.fields import ColorField
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db.models import (
    SET_NULL,
    BooleanField,
    CASCADE,
    CharField,
    F,
    ForeignKey,
    IntegerField,
    OuterRef,
    TextField,
    URLField,
)
from django.db.models.functions import Cast
from django_comments_xtd import get_model as get_comment_model
from django_tables2 import RequestConfig
from hitcount.models import HitCount, HitCountMixin
from hitcount.views import HitCountMixin as HitCountViewMixin
from modelcluster.contrib.taggit import ClusterTaggableManager
from star_ratings.models import Rating
from taggit.models import ItemBase, TagBase
from treenode.models import TreeNodeModel
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, MultipleChooserPanel
from wagtail.blocks import RawHTMLBlock, RichTextBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page, ParentalKey
from wagtail.search.index import AutocompleteField, Indexed, RelatedFields, SearchField
from wagtail.snippets.models import register_snippet

from edx_operation.apps.core.utils.common import SubqueryCount, random_color


XtdComment = get_comment_model()


@register_snippet
class Tag(TagBase):
    """Tag."""

    class Meta:
        """Meta."""

        verbose_name = "태그"
        verbose_name_plural = verbose_name
        unique_together = ("name",)

    color = ColorField("태그 컬러", default=random_color, format="hexa")


class TaggedPageItem(ItemBase):
    """TaggedPageItem."""

    content_object = ParentalKey(Page, on_delete=CASCADE)
    tag = ForeignKey(Tag, on_delete=CASCADE)


@register_snippet
class Category(Indexed, TreeNodeModel):
    """Category."""

    class Meta(TreeNodeModel.Meta):
        """Meta."""

        verbose_name = "카테고리"
        verbose_name_plural = verbose_name

    treenode_display_field = "name"

    name = CharField(max_length=50, db_index=True)
    description = TextField("설명", null=True, blank=True)

    search_fields = [
        SearchField("name"),
        AutocompleteField("name"),
    ]

    def clean(self):
        """clean."""
        if self.parent:
            no_cache_qs = self.parent.get_children_queryset()
        else:
            no_cache_qs = self.get_roots_queryset()

        if self.name in no_cache_qs.exclude(pk=self.pk).values_list("name", flat=True):
            raise ValidationError("같은 레벨에 중복된 이름이 있습니다.")


class CategorizedPageItem(Orderable):
    """CategorizedPageItem."""

    content_object = ParentalKey(Page, on_delete=CASCADE, related_name="categories")
    category = ForeignKey(Category, on_delete=CASCADE)


class AbstractPostHome(Page):
    """AbstractPostHome."""

    class Meta:
        """Meta."""

        abstract = True

    subpage_types = []
    max_count = 1
    show_in_menus_default = True

    # fmt: off

    cover = ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=SET_NULL, related_name="+")
    short_description = TextField("간략한 설명", null=True, blank=True)
    content = RichTextField("내용", null=True, blank=True)

    # fmt: on

    content_panels = Page.content_panels + [
        FieldPanel("cover"),
        FieldPanel("short_description"),
        FieldPanel("content"),
    ]

    def get_context(self, request, *args, **kwargs):
        """get_context.

        :param request:
        :param args:
        :param kwargs:
        """
        context = super().get_context(request, *args, **kwargs)

        # all posts
        posts = self.get_children_with_annotation().live().order_by("-priority", f"-id")

        # search
        search = request.GET.get("search")
        if search:
            posts = posts.search(search)

        # django tables
        from .tables import PageTable

        post_table = PageTable(posts)

        # filter, sort, pagination
        RequestConfig(request).configure(post_table)

        context.update(post_table=post_table)
        return context

    def get_children_with_annotation(self):
        """get_children_with_annotation."""
        # if not raise
        subpage_type = self.subpage_types[0].lower()
        return self.get_children().annotate(
            # priority
            priority=F(f"{subpage_type}__priority"),
            # annotate hits
            hit_count=F(f"{subpage_type}__hit__hits"),
            # annotate ratings
            rating_count=F(f"{subpage_type}__rating__count"),
            # annotate ratings
            comment_count=SubqueryCount(
                XtdComment.objects.filter(
                    content_type=OuterRef("content_type"),
                    object_pk=Cast(OuterRef("pk"), output_field=CharField()),
                )
            ),
            # XtdComment.object_id 가 CharField를 사용하기 때문에 GenericRelation을 사용할 수 없음
            # comment_count=Count(f"{subpage_type}__comments__pk"),
        )


class AbstractPostPage(Page, HitCountMixin):
    """AbstractPostPage."""

    class Meta:
        """Meta."""

        abstract = True

    parent_page_types = []
    subpage_types = []

    content = StreamField(
        [
            ("richtext", RichTextBlock(label="에디터", required=False)),
            ("html", RawHTMLBlock(label="HTML 코드", required=False)),
        ],
        null=True,
        blank=True,
        verbose_name="내용",
        use_json_field=True,
    )
    priority = IntegerField("상단 정렬", default=0)
    external_link = URLField("외부 링크", max_length=254, null=True, blank=True)
    allow_comments = BooleanField("댓글 사용하기", default=True)
    tags = ClusterTaggableManager("태그", through=TaggedPageItem, blank=True)

    hit = GenericRelation(HitCount, object_id_field="object_pk")  # OneToOne
    rating = GenericRelation(Rating)  # OneToOne
    comments = GenericRelation(XtdComment, object_id_field="object_pk")  # ManyToMany

    search_fields = Page.search_fields + [
        SearchField("content"),
        SearchField("first_published_at"),
        SearchField("last_published_at"),
        RelatedFields("tags", [SearchField("name")]),
        RelatedFields("owner", [SearchField("username"), SearchField("full_name")]),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("content"),
                FieldPanel("priority", classname="collapsed"),
                FieldPanel("external_link"),
                FieldPanel("allow_comments"),
                FieldPanel("tags"),
                MultipleChooserPanel("categories", "category", label="카테고리"),
            ],
            heading="페이지 내용",
        )
    ]

    @property
    def hit_count(self):
        """hit_count."""
        # fix: page preview mode
        return super().hit_count if self.pk else HitCount()

    def serve(self, request, *args, **kwargs):
        """serve.

        :param request:
        :param args:
        :param kwargs:
        """
        # update hit
        hit_count = self.hit.get_for_object(self)
        HitCountViewMixin.hit_count(request, hit_count)
        return super().serve(request, *args, **kwargs)

    def get_absolute_url(self):
        """get_absolute_url."""
        return self.full_url
