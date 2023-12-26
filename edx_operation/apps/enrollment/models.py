from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    SmallIntegerField,
    TextField,
)
from django_extensions.db.models import TimeStampedModel

from edx_operation.apps.course.models import CourseRun
from edx_operation.apps.student.models import Student


class Enrollment(TimeStampedModel):
    class Meta:
        verbose_name = "수강"
        verbose_name_plural = verbose_name
        unique_together = (("courserun", "student"),)

    # fmt: off

    courserun = ForeignKey(CourseRun, on_delete=CASCADE, verbose_name="과정 회차")
    student = ForeignKey(Student, on_delete=CASCADE, verbose_name="학습자")
    mode = CharField("수강 모드", max_length=50, null=True, blank=True)
    is_active = BooleanField("활성", default=False)

    study_start = DateTimeField("학습 시작", null=True, blank=True)
    study_end = DateTimeField("학습 종료", null=True, blank=True)
    review_period = SmallIntegerField("복습 기간", default=0)

    # fmt: on


class Collection(TimeStampedModel):
    class Meta:
        verbose_name = "컬렉션"
        verbose_name_plural = verbose_name

    # fmt: off

    display_name = CharField("제목", max_length=255, unique=True)
    description = TextField("설명", null=True, blank=True)
    courseruns = ManyToManyField(CourseRun, verbose_name="과정 회차", blank=True)
    is_active = BooleanField("활성", default=False)

    # fmt: on


class CollectionEntitlement(TimeStampedModel):
    class Meta:
        verbose_name = "컬렉션 등록"
        verbose_name_plural = verbose_name

    # fmt: off

    collection = ForeignKey(Collection, on_delete=CASCADE, verbose_name="컬렉션")
    student = ForeignKey(Student, on_delete=CASCADE, verbose_name="학습자")
    is_active = BooleanField("활성", default=True)

    start = DateTimeField("시작", null=True, blank=True, db_index=True)
    end = DateTimeField("종료", null=True, blank=True, db_index=True)
