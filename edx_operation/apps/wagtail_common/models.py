from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from django.db.models import CharField, TextField
from django.db.models import CASCADE, ForeignKey
from taggit.managers import TaggableManager
from taggit.models import CommonGenericTaggedItemBase, TagBase
from treenode.models import TreeNodeModel
from wagtail.snippets.models import register_snippet

from edx_operation.apps.core.utils.common import random_color


@register_snippet
class Tag(TagBase):
    """Tag."""

    class Meta:
        """Meta."""

        verbose_name = "태그"
        verbose_name_plural = verbose_name
        unique_together = ("name",)

    color = ColorField("태그 컬러", default=random_color, format="hexa")


class Tagging(CommonGenericTaggedItemBase):
    """Tagging."""

    class Meta:
        """Meta."""

        verbose_name = "태깅"
        verbose_name_plural = verbose_name

    object_id = CharField(max_length=50, db_index=True)
    tag = ForeignKey(Tag, on_delete=CASCADE, related_name="%(app_label)s_%(class)s_items")


@register_snippet
class Category(TreeNodeModel):
    """Category."""

    class Meta(TreeNodeModel.Meta):
        """Meta."""

        verbose_name = "카테고리"
        verbose_name_plural = verbose_name

    treenode_display_field = "name"

    # fmt: off

    name = CharField(max_length=50, db_index=True)
    description = TextField("설명", null=True, blank=True)
    tags = TaggableManager("태그", through=Tagging, blank=True)

    # fmt: on

    def clean(self):
        """clean."""
        if self.parent:
            no_cache_qs = self.parent.get_children_queryset()
        else:
            no_cache_qs = self.get_roots_queryset()

        if self.name in no_cache_qs.exclude(pk=self.pk).values_list("name", flat=True):
            raise ValidationError("같은 레벨에 중복된 이름이 있습니다.")
