from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    DateTimeField,
    FloatField,
    ForeignKey,
    JSONField,
    PositiveIntegerField,
    UUIDField,
)
from django_extensions.db.models import TimeStampedModel
from opaque_keys.edx.django.models import UsageKeyField
from opaque_keys.edx.django.models import UsageKeyField
from edx_operation.apps.course.models import Block, CourseRun, Subsection
from edx_operation.apps.student.models import Student


class CourseRunGrade(TimeStampedModel):
    class Meta:
        verbose_name = "성적"
        verbose_name_plural = verbose_name
        unique_together = (("courserun", "student"),)

    # fmt: off

    courserun = ForeignKey(CourseRun, on_delete=CASCADE, verbose_name="회차")
    student = ForeignKey(Student, on_delete=CASCADE, verbose_name="학습자")
    percent_grade = FloatField("점수", null=True, blank=True)
    letter_grade = CharField("평점", max_length=255, null=True, blank=True)
    passed = BooleanField("수료", null=True, blank=True)
    grade_summary = JSONField("상세", null=True, blank=True)

    # fmt: on


class SubsectionGrade(TimeStampedModel):
    class Meta:
        verbose_name = "차시 성적"
        verbose_name_plural = verbose_name
        unique_together = (("subsection", "student"),)

    # fmt: off

    subsection = ForeignKey(Subsection, on_delete=CASCADE, verbose_name="차시")
    student = ForeignKey(Student, on_delete=CASCADE, verbose_name="학습자")
    earned_all = FloatField("득점", null=True, blank=True)
    possible_all = FloatField("총점", null=True, blank=True)
    earned_graded = FloatField("득점(성적)", null=True, blank=True)
    possible_graded = FloatField("총점(성적)", null=True, blank=True)
    due = DateTimeField("마감", null=True, blank=True)
    complete = BooleanField("완료", null=True, blank=True)
    completion_block = UsageKeyField("학습 위치", max_length=255, null=True, blank=True)
    client_ip = CharField("학습자 ip", max_length=50, null=True, blank=True)

    # fmt: on


class ExamStatus(TimeStampedModel):
    class Meta:
        verbose_name = "시험"
        verbose_name_plural = verbose_name
        unique_together = (("subsection", "student"),)

    # fmt: off

    subsection = ForeignKey(Subsection, on_delete=CASCADE, verbose_name="차시")
    student = ForeignKey(Student, on_delete=CASCADE, verbose_name="학습자")
    is_active = BooleanField("활성", null=True, blank=True)
    status = CharField("상태", max_length=50, null=True, blank=True)
    deleted = BooleanField("삭제", null=True, blank=True)

    # fmt: on


class Submission(TimeStampedModel):
    class Meta:
        verbose_name = "답안 제출"
        verbose_name_plural = verbose_name
        index_together = (("block", "student"),)

    # fmt: off

    uuid = UUIDField(unique=True)
    block = ForeignKey(Block, on_delete=CASCADE, verbose_name="블록")
    student = ForeignKey(Student, on_delete=CASCADE, verbose_name="학습자")
    attempt_number = PositiveIntegerField("시도", default=1)
    submitted_at = DateTimeField("제출", null=True, blank=True)
    answer = JSONField("답안", null=True, blank=True)
    status = CharField("상태", max_length=10, null=True, blank=True, choices=(("D", "Deleted"), ("A", "Active")))

    points_earned = PositiveIntegerField("득점", default=0)
    points_possible = PositiveIntegerField("배점", default=0)
    scored_at = DateTimeField("채점 시간", null=True, blank=True)
    score_reset = BooleanField("점수 초기화", null=True, blank=True)

    # fmt: off
