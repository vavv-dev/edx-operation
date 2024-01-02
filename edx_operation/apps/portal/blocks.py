from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    RawHTMLBlock,
    RichTextBlock,
    StructBlock,
)
from wagtail.images.blocks import ImageChooserBlock

from edx_operation.apps.wagtail_common.models import Tag


class DynamicChoiceBlock(ChoiceBlock):
    """DynamicChoiceBlock."""

    tag_filter = None

    def __init__(self, *args, tag_filter=None, **kwargs):
        """__init__.

        :param args:
        :param tag_filter:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.tag_filter = tag_filter

    def _get_callable_choices(self, choices, blank_choice=True):
        """_get_callable_choices.

        :param choices:
        :param blank_choice:
        """

        def choices_callable():
            """choices_callable."""
            return [
                (tag, tag.name)
                for tag in Tag.objects.filter(
                    taggedpageitem__content_object__content_type__model=self.tag_filter
                ).distinct()
            ]

        return choices_callable


class TaggedContentBlock(StructBlock):
    """TaggedContentBlock."""

    class Meta:
        """Meta."""

    # dynamic choices로 변경
    # tag = DynamicChoiceBlock(label="태그", choices=[])

    title = CharBlock(required=True, label="제목")
    sub_title = CharBlock(required=False, label="부제목")
    image = ImageChooserBlock(required=False, label="이미지")

    def __str__(self):
        """__str__."""
        return str(self.title)

    def __init__(self, tag_filter, local_blocks=None, **kwargs):
        """__init__.

        base blocks가 singleton으로 작동해서 StreamField에서 dynamic하게 사용할 수 없음
        multipleton으로 변경하고 dynamic choices를 적용함

        :param tag_filter:
        :param local_blocks:
        :param kwargs:
        """

        tag = DynamicChoiceBlock(label="태그", choices=[], tag_filter=tag_filter)
        tag.name = "tag"

        self.base_blocks["tag"] = tag
        self.base_blocks.move_to_end("tag", False)

        super().__init__(**kwargs)


class BannerBlock(StructBlock):
    class Meta:
        label = "메인 배너"

    image = ImageChooserBlock(label="배너")
    fit_container = BooleanBlock(label="container에 맞추기", required=False)
    title = CharBlock(label="제목")
    content = RichTextBlock(label="에디터", required=False)
    html = RawHTMLBlock(label="HTML", required=False)

    def __str__(self):
        return str(self.title)
