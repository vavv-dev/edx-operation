from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    JSONField,
    Model,
    OneToOneField,
    SmallIntegerField,
    TextField,
)
from django_extensions.db.models import TimeStampedModel

from edx_operation.apps.course.models import CourseRun
from edx_operation.apps.student.models import Student


class Operation(TimeStampedModel):
    class Meta:
        verbose_name = "운영"
        verbose_name_plural = verbose_name

    courserun = OneToOneField(CourseRun, on_delete=CASCADE, verbose_name="회차")
    shut_downed = BooleanField("운영 종료", default=False)

    def shut_down(self):
        pass

    # TODO 여기에 운영에 관한 기능 구현


class CourseRunAccessRole(TimeStampedModel):
    class Meta:
        verbose_name = "수강 권한"
        verbose_name_plural = verbose_name
        unique_together = ("org", "courserun", "student", "role")

    # fmt: off

    courserun = ForeignKey(CourseRun, on_delete=CASCADE, verbose_name="회차", null=True, blank=True)
    student = ForeignKey(Student, on_delete=CASCADE, verbose_name="학습자")
    org = CharField("분류", max_length=64, db_index=True, null=True, blank=True)
    role = CharField("권한", max_length=64, db_index=True)

    # fmt: on


class Post(Model):
    """Post."""

    class Meta:
        """Meta."""

        verbose_name = "질문 답변"
        verbose_name_plural = verbose_name

    # fmt: off

    id = CharField(max_length=50, primary_key=True)
    title = CharField("제목", max_length=255, null=True, blank=True)
    body = TextField("내용", null=True, blank=True)
    annoymous = BooleanField("익명", null=True, blank=True)
    # 댓글일 때는 courserun이 없음
    courserun = ForeignKey(CourseRun, on_delete=CASCADE, verbose_name="과정 회차", null=True, blank=True)
    student = ForeignKey(Student, on_delete=CASCADE, verbose_name="학습자")
    thread = ForeignKey("self", on_delete=CASCADE, verbose_name="쓰레드",  null=True, blank=True, related_name="comments")
    parent = ForeignKey("self", on_delete=CASCADE, verbose_name="부모글", null=True, blank=True, related_name="children")
    depth = SmallIntegerField("단계", null=True, blank=True)
    commentable_id = CharField("게시판 위치", max_length=255)
    thread_type = CharField("종류", max_length=50, null=True, blank=True)
    created_at = DateTimeField("생성", null=True, blank=True)
    updated_at = DateTimeField("수정", null=True, blank=True)
    closed = BooleanField("종료", null=True, blank=True)
    votes = JSONField("추천", null=True, blank=True)
    type = CharField("형식", max_length=50, null=True, blank=True)
    deleted = BooleanField("삭제", null=True, blank=True)

    # fmt: on
