# Generated by Django 4.2 on 2023-12-25 18:21

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import opaque_keys.edx.django.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("course", "0001_initial"),
        ("student", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubsectionGrade",
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
                    "earned_all",
                    models.FloatField(blank=True, null=True, verbose_name="득점"),
                ),
                (
                    "possible_all",
                    models.FloatField(blank=True, null=True, verbose_name="총점"),
                ),
                (
                    "earned_graded",
                    models.FloatField(blank=True, null=True, verbose_name="득점(성적)"),
                ),
                (
                    "possible_graded",
                    models.FloatField(blank=True, null=True, verbose_name="총점(성적)"),
                ),
                ("due", models.DateTimeField(blank=True, null=True, verbose_name="마감")),
                (
                    "complete",
                    models.BooleanField(blank=True, null=True, verbose_name="완료"),
                ),
                (
                    "completion_block",
                    opaque_keys.edx.django.models.UsageKeyField(
                        blank=True, max_length=255, null=True, verbose_name="학습 위치"
                    ),
                ),
                (
                    "client_ip",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="학습자 ip"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="student.student",
                        verbose_name="학습자",
                    ),
                ),
                (
                    "subsection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.subsection",
                        verbose_name="차시",
                    ),
                ),
            ],
            options={
                "verbose_name": "차시 성적",
                "verbose_name_plural": "차시 성적",
                "unique_together": {("subsection", "student")},
            },
        ),
        migrations.CreateModel(
            name="Submission",
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
                ("uuid", models.UUIDField(unique=True)),
                (
                    "attempt_number",
                    models.PositiveIntegerField(default=1, verbose_name="시도"),
                ),
                (
                    "submitted_at",
                    models.DateTimeField(blank=True, null=True, verbose_name="제출"),
                ),
                ("answer", models.JSONField(blank=True, null=True, verbose_name="답안")),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[("D", "Deleted"), ("A", "Active")],
                        max_length=10,
                        null=True,
                        verbose_name="상태",
                    ),
                ),
                (
                    "points_earned",
                    models.PositiveIntegerField(default=0, verbose_name="득점"),
                ),
                (
                    "points_possible",
                    models.PositiveIntegerField(default=0, verbose_name="배점"),
                ),
                (
                    "scored_at",
                    models.DateTimeField(blank=True, null=True, verbose_name="채점 시간"),
                ),
                (
                    "score_reset",
                    models.BooleanField(blank=True, null=True, verbose_name="점수 초기화"),
                ),
                (
                    "block",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.block",
                        verbose_name="블록",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="student.student",
                        verbose_name="학습자",
                    ),
                ),
            ],
            options={
                "verbose_name": "답안 제출",
                "verbose_name_plural": "답안 제출",
                "index_together": {("block", "student")},
            },
        ),
        migrations.CreateModel(
            name="ExamStatus",
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
                    "is_active",
                    models.BooleanField(blank=True, null=True, verbose_name="활성"),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="상태"
                    ),
                ),
                (
                    "deleted",
                    models.BooleanField(blank=True, null=True, verbose_name="삭제"),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="student.student",
                        verbose_name="학습자",
                    ),
                ),
                (
                    "subsection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.subsection",
                        verbose_name="차시",
                    ),
                ),
            ],
            options={
                "verbose_name": "시험",
                "verbose_name_plural": "시험",
                "unique_together": {("subsection", "student")},
            },
        ),
        migrations.CreateModel(
            name="CourseRunGrade",
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
                    "percent_grade",
                    models.FloatField(blank=True, null=True, verbose_name="점수"),
                ),
                (
                    "letter_grade",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="평점"
                    ),
                ),
                (
                    "passed",
                    models.BooleanField(blank=True, null=True, verbose_name="수료"),
                ),
                (
                    "grade_summary",
                    models.JSONField(blank=True, null=True, verbose_name="상세"),
                ),
                (
                    "courserun",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course.courserun",
                        verbose_name="회차",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="student.student",
                        verbose_name="학습자",
                    ),
                ),
            ],
            options={
                "verbose_name": "성적",
                "verbose_name_plural": "성적",
                "unique_together": {("courserun", "student")},
            },
        ),
    ]
