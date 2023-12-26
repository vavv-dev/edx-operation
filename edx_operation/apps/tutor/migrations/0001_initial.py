# Generated by Django 4.2 on 2023-12-25 18:21

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import edx_operation.apps.core.utils.common
import edx_operation.apps.tutor.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("grade", "0001_initial"),
        ("core", "0001_initial"),
        ("enrollment", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Scoring",
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
                (
                    "client_ip",
                    models.GenericIPAddressField(
                        blank=True, null=True, verbose_name="IP 주소"
                    ),
                ),
                (
                    "submission",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="grade.submission",
                        verbose_name="제출",
                    ),
                ),
            ],
            options={
                "verbose_name": "채점",
                "verbose_name_plural": "채점",
            },
        ),
        migrations.CreateModel(
            name="TutorInfo",
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
                ("is_active", models.BooleanField(default=True, verbose_name="활성")),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=edx_operation.apps.core.utils.common.upload_unique_name,
                        verbose_name="이미지",
                    ),
                ),
                ("bio", models.TextField(blank=True, null=True, verbose_name="학력/경력")),
            ],
            options={
                "verbose_name": "튜터 정보",
                "verbose_name_plural": "튜터 정보",
            },
        ),
        migrations.CreateModel(
            name="Tutor",
            fields=[],
            options={
                "verbose_name": "튜터",
                "verbose_name_plural": "튜터",
                "permissions": (("tutor", "튜터"),),
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.user",),
            managers=[
                ("objects", edx_operation.apps.tutor.models.TutorManager()),
                ("user_objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Tutoring",
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
                (
                    "enrollment",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="enrollment.enrollment",
                        verbose_name="수강",
                    ),
                ),
                (
                    "tutorinfo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tutor.tutorinfo",
                        verbose_name="튜터",
                    ),
                ),
            ],
            options={
                "verbose_name": "튜터링",
                "verbose_name_plural": "튜터링",
            },
        ),
        migrations.AddField(
            model_name="tutorinfo",
            name="enrollments",
            field=models.ManyToManyField(
                blank=True,
                through="tutor.Tutoring",
                to="enrollment.enrollment",
                verbose_name="담당 수강",
            ),
        ),
        migrations.AddField(
            model_name="tutorinfo",
            name="scorings",
            field=models.ManyToManyField(
                blank=True,
                through="tutor.Scoring",
                to="grade.submission",
                verbose_name="담당 채점",
            ),
        ),
        migrations.AddField(
            model_name="tutorinfo",
            name="tutor",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="tutor.tutor",
                verbose_name="튜터",
            ),
        ),
        migrations.AddField(
            model_name="scoring",
            name="tutorinfo",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="tutor.tutorinfo",
                verbose_name="튜터",
            ),
        ),
    ]
