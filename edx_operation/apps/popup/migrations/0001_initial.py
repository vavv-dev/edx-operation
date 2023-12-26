# Generated by Django 4.2 on 2023-12-25 18:24

import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import taggit.managers
import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.search.index


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wagtail_common", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Popup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("is_active", models.BooleanField(default=False, verbose_name="활성")),
                (
                    "login_required",
                    models.BooleanField(default=False, verbose_name="로그인 필요"),
                ),
                (
                    "title",
                    models.CharField(db_index=True, max_length=254, verbose_name="제목"),
                ),
                (
                    "content",
                    wagtail.fields.StreamField(
                        [
                            (
                                "image",
                                wagtail.images.blocks.ImageChooserBlock(
                                    label="이미지", required=False
                                ),
                            ),
                            (
                                "richtext",
                                wagtail.blocks.RichTextBlock(
                                    label="텍스트", required=False
                                ),
                            ),
                            (
                                "embed",
                                wagtail.embeds.blocks.EmbedBlock(
                                    label="임베드", required=False
                                ),
                            ),
                            (
                                "html",
                                wagtail.blocks.RawHTMLBlock(
                                    help_text="html 코드를 입력할 수 있습니다.",
                                    label="HTML",
                                    required=False,
                                ),
                            ),
                        ],
                        use_json_field=True,
                        verbose_name="내용",
                    ),
                ),
                ("counter", models.IntegerField(default=0, verbose_name="조회수")),
                ("start", models.DateTimeField(verbose_name="게시 시작")),
                ("end", models.DateTimeField(verbose_name="게시 종료")),
                (
                    "background_color",
                    colorfield.fields.ColorField(
                        default="#FAFAFA",
                        image_field=None,
                        max_length=25,
                        samples=None,
                        verbose_name="배경색",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="작성자",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text="A comma-separated list of tags.",
                        through="wagtail_common.Tagging",
                        to="wagtail_common.Tag",
                        verbose_name="태그",
                    ),
                ),
            ],
            options={
                "verbose_name": "팝업",
                "verbose_name_plural": "팝업",
            },
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
    ]