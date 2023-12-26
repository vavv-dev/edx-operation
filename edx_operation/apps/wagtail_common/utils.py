from wagtail.blocks import RawHTMLBlock, RichTextBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock


def StreamFieldFactory(verbose_name, null=False, blank=False):
    return StreamField(
        [
            ("image", ImageChooserBlock(label="이미지", required=False)),
            ("richtext", RichTextBlock(label="텍스트", required=False)),
            ("embed", EmbedBlock(label="임베드", required=False)),
            ("html", RawHTMLBlock(label="HTML", required=False, help_text="html 코드를 입력할 수 있습니다."),),  # fmt:skip
        ],
        verbose_name=verbose_name,
        null=null,
        blank=blank,
        use_json_field=True,
    )
