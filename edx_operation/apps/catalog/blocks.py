from wagtail.blocks import CharBlock, ChoiceBlock, IntegerBlock, StructBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock


class CatalogPageBackgroundBlock(StructBlock):
    image = ImageChooserBlock(
        label="페이지 배경 이미지",
        help_text="300dpi A4 사이즈: 2481x3507 픽셀, 600dpi A4 사이즈: 4962x7014 픽셀",
    )
    apply_to_pages = ChoiceBlock(
        label="적용할 페이지",
        choices=(
            ("odd", "홀수 페이지"),
            ("even", "짝수 페이지"),
            ("all", "모든 페이지"),
        ),
        required=False,
    )
    apply_to_specific_pages = CharBlock(
        label="적용할 특정 페이지",
        required=False,
        help_text="ex. 11, 23, 22",
    )

    class Meta:
        label = "카탈로그 페이지 배경"


class CatalogPageLogoBlock(StructBlock):
    image = ImageChooserBlock(
        label="페이지 로고 이미지",
        help_text="300dpi 세로 1cm 사이즈: 118 픽셀, 600dpi 세로 1cm 사이즈: 236 픽셀",
    )
    apply_to_pages = ChoiceBlock(
        label="적용할 페이지",
        choices=(
            ("odd", "홀수 페이지"),
            ("even", "짝수 페이지"),
            ("all", "모든 페이지"),
        ),
        required=False,
    )
    apply_to_specific_pages = CharBlock(
        label="적용할 특정 페이지",
        required=False,
        help_text="ex. 11, 23, 22",
    )

    class Meta:
        label = "카탈로그 로고"


class CatalogImagePageBlock(StructBlock):
    title = CharBlock(
        label="페이지 제목",
        help_text="목차에 표시될 페이지 제목",
    )
    image = ImageChooserBlock(
        label="페이지 이미지",
        help_text="300dpi A4 사이즈: 2481x3507 픽셀, 600dpi A4 사이즈: 4962x7014 픽셀",
    )
    insert_to = IntegerBlock(label="삽입할 위치 페이지 번호")

    class Meta:
        label = "카탈로그 이미지 페이지"


class FinancialAssistanceBlock(StructBlock):
    policy = CharBlock(label="지원 제도")
    benefit = TableBlock(label="지원 내용")

    class Meta:
        label = "교육비 지원"
