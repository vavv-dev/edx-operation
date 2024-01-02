from wagtail.blocks import CharBlock, DateBlock, IntegerBlock, RichTextBlock, StructBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock


class TuitionAssistanceBlock(StructBlock):
    policy = CharBlock(label="교육비 지원 제도")
    assistance = TableBlock(label="지원 내용")

    class Meta:
        label = "교육비 지원"


class TutorBlock(StructBlock):
    image = ImageChooserBlock(required=False, label="사진")
    name = CharBlock(label="이름")
    bio = RichTextBlock(required=False, label="바이오")

    class Meta:
        label = "교수진"


class TextbookBlock(StructBlock):
    title = CharBlock(label="제목")
    author = CharBlock(label="저자")
    publisher = CharBlock(label="출판사")
    published_date = DateBlock(required=False, label="출간일")
    isbn = CharBlock(label="ISBN")
    price = IntegerBlock(label="가격")

    class Meta:
        label = "교재"
