import os
import random
import string

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    DateField,
    DateTimeField,
    FileField,
    FloatField,
    ForeignKey,
    ImageField,
    IntegerField,
    JSONField,
    Max,
    Model,
    OneToOneField,
    PositiveIntegerField,
    SET_NULL,
    SmallIntegerField,
    TextField,
    URLField,
)
from django.utils.timezone import localtime
from django_extensions.db.models import TimeStampedModel
from opaque_keys.edx.django.models import CourseKeyField, UsageKeyField
from opaque_keys.edx.keys import UsageKey
from opaque_keys.edx.locator import CourseLocator
from requests import HTTPError

from edx_operation.apps.api_client.jwt import CmsAPIClient, LmsAPIClient
from edx_operation.apps.core.constants import EMPTY_COURSE_DISPLAY_NAME as EMPTY
from edx_operation.apps.core.utils.common import (
    DateUtils,
    admin_action,
    upload_unique_name as upload_to,
)

from .service import CourseCreator


def random_number():
    return Course.random_number()


class Course(TimeStampedModel):
    class Meta:
        verbose_name = "과정"
        verbose_name_plural = verbose_name

    # fmt: off

    id = CharField("과정 코드", max_length=50, primary_key=True, default=random_number)
    display_name = CharField("제목", max_length=255, db_index=True)
    cover = ImageField("커버 이미지", max_length=255, upload_to=upload_to)
    is_active = BooleanField("활성", default=False)
    description = TextField("설명", null=True, blank=True)
    target = TextField("대상", null=True, blank=True)
    objective = TextField("학습목표", null=True, blank=True)
    grading = TextField("평가 방법", null=True, blank=True)
    created_date = DateField("출시", null=True, blank=True)
    preview = URLField("미리보기", null=True, blank=True)
    contents = TextField("목차", null=True, blank=True)
    effort = CharField("학습 시간", max_length=20, null=True, blank=True)
    level = CharField("레벨", max_length=20, null=True, blank=True)
    ncs_unit = CharField("NCS 분류", max_length=254, null=True, blank=True)

    # fmt: on

    def __str__(self) -> str:
        return f"{self.display_name}"

    @classmethod
    def random_number(cls):
        number = None
        while True:
            number = "".join(random.choices(string.ascii_lowercase, k=8))
            if not cls.objects.filter(id=number).exists():
                break
        return number

    @admin_action
    def update_contents(self, courserun=None):
        if not courserun:
            courserun = self.courserun_set.first()
        self.contents = "\n".join(
            Subsection.objects.filter(chapter__courserun=courserun)
            .values_list("display_name", flat=True)
            .order_by("sequence")
        )
        self.save()

    @admin_action
    def update_grading(self, courserun=None):
        if not courserun:
            courserun = self.courserun_set.first()

        if courserun.pass_on_progress:
            self.grading = f"진도율 {courserun.pass_on_progress}% 이상 수료"
        else:
            self.grading = " | ".join(
                [
                    f"{exam} {cutoff * 100:0.0f}%"
                    for exam, cutoff in reversed(courserun.grading.items())
                    if cutoff
                ]
            )
        self.save()

    def next_course_run_number(self):
        last_run_number = self.courserun_set.aggregate(Max("run_number"))["run_number__max"]
        return last_run_number + 1 if last_run_number is not None else 1


class CourseRun(TimeStampedModel):
    class Meta:
        verbose_name = "회차"
        verbose_name_plural = verbose_name
        unique_together = (("course", "run_number"),)

    # fmt: off

    id = CourseKeyField("회차 코드", max_length=255, primary_key=True)
    course = ForeignKey(Course, on_delete=CASCADE, verbose_name="과정")
    run_number = PositiveIntegerField("회차 번호", null=True, blank=True)

    display_name = CharField("제목", max_length=255, db_index=True)
    enrollment_start = DateTimeField("등록 시작", null=True, blank=True, db_index=True)
    enrollment_end = DateTimeField("등록 종료", null=True, blank=True, db_index=True)
    start = DateTimeField("시작", null=True, blank=True, db_index=True)
    end = DateTimeField("종료", null=True, blank=True, db_index=True)
    invitation_only = BooleanField("자율등록 허용 안함", default=True)
    visible_to_staff_only = BooleanField("학습자에게 비공개", default=False)
    certificate_available_date = DateTimeField("수료증 발급", null=True, blank=True)
    pacing = CharField("학습 방법", max_length=50, null=True, blank=True, db_index=True)
    grading = JSONField("평가 방법", default=dict)

    verification_method = CharField("본인 인증 방법", max_length=100, null=True, blank=True)
    entrance_id_verification = BooleanField("입과 시 인증", default=True)
    course_verification = BooleanField("매 8차시 진행, 진행평가, 시험, 과제 학습 시 인증", default=True)
    study_in_order = BooleanField("순차 학습 적용", default=True)
    daily_study_limit = IntegerField("일일 학습 제한 차시", default=8, help_text="0: 제한 하지 않습니다.")
    block_multiple_window = BooleanField("동시 학습 창 제한", default=True)
    exam_prerequisite_progress = IntegerField("시험/과제 응시 진도 조건 %", default=80)
    exam_prerequisite_midterm_exam = BooleanField("시험/과제 응시 진행평가 완료 조건", default=True)
    block_exam_on_mobile = BooleanField("시험/과제 응시 모바일 제한", default=True)
    block_exam_on_tablet = BooleanField("시험/과제 응시 태블릿 제한", default=True)
    exam_reattempt_days = IntegerField("재시험 허용 일", default=0, help_text="0: 허용하지 않음")
    ignore_certificate_available_date = BooleanField("수료증 발급 날짜 무시", default=False)
    pass_on_progress = IntegerField("진도율로 수료 처리", default=0)

    # fmt: on

    def __str__(self):
        return f"{self.pk}"

    @classmethod
    def random_run(cls, org, number):
        run = None
        while True:
            suffix = "".join(random.choices(string.ascii_uppercase, k=2))
            run = localtime().strftime("%Y%m%d") + suffix
            courserun_id = CourseLocator(org=org, course=number, run=run)
            if not cls.objects.filter(id=courserun_id).exists():
                break
        return run

    @admin_action
    def rerun(self, start=None, end=None, title_override=None):
        if not start:
            start = DateUtils.day_start() + relativedelta(days=1)
        if not end:
            end = start + relativedelta(months=1, seconds=-1)
        if not title_override:
            title_override = self.display_name

        new_run = self.random_run(org=self.id.org, number=self.id.course)
        new_courserun_id = self.id.replace(run=new_run)
        source_courserun_id = self.id

        # copy source CourseRun
        self.id = new_courserun_id
        self.run_number = self.course.next_course_run_number()
        self.display_name = EMPTY
        self.created = self.modified = None
        self.start = self.enrollment_start = self.certificate_available_date = start
        self.end = self.enrollment_end = end
        self.save()

        # cf. cms/djangoapps/contentstore/views/course.py:1060
        # enrollment_start, enrollment_end not working

        # api client
        CmsAPIClient().v1_course_runs_rerun(
            source_courserun_id,
            {
                "run": new_run,
                "title": title_override,
                "pacing_type": f"{self.pacing}_paced",
                "schedule": {
                    "start": str(start),
                    "end": str(end),
                    "enrollment_start": str(start),
                    "enrollment_end": str(end),
                },
            },
        )

    @admin_action
    def sync_courserun_blocks(self):
        lms_client = LmsAPIClient()
        course_blocks = lms_client.courses_v2_blocks_list(
            self.id,
            {
                "all_blocks": True,
                "depth": "all",
                "requested_fields": "format,children,special_exam_info",
                "allow_start_dates_in_future": True,
            },
        )

        # grading policy
        policies = lms_client.grades_v1_policy_courses_read(self.id)
        policies = {
            policy.get("assignment_type"): policy.get("weight")
            / (policy.get("count") - policy.get("dropped"))
            for policy in policies
            if policy.get("count") - policy.get("dropped")
        }

        self.grading = policies
        self.save()

        # blocks
        blocks = course_blocks.get("blocks")
        course_block = blocks.get(course_blocks.get("root"))

        # subsection sequence
        sequence = 1

        # subsection's all children
        def get_all_children(block):
            """get_all_children.

            :param block:
            """
            if "children" not in blocks[block]:
                return set()

            children = blocks[block]["children"]
            all_children = set(children)

            for child in children:
                all_children.update(get_all_children(child))

            return all_children

        chapters = []
        subsections = []
        actual_blocks = []

        cms_client = CmsAPIClient()

        for i, chapter_key_str in enumerate(course_block.get("children") or [], start=1):
            chapter_block = blocks.get(chapter_key_str)
            if not chapter_block or chapter_block.get("type") != "chapter":
                continue

            # chapters
            chapter_usage_key = UsageKey.from_string(chapter_key_str)
            chapters.append(
                Chapter(
                    id=chapter_usage_key,
                    courserun_id=self.id,
                    display_name=chapter_block.get("display_name"),
                    sequence=i,
                )
            )

            for subsection_key_str in chapter_block.get("children") or []:
                subsection_block = blocks.get(subsection_key_str)
                if not subsection_block or subsection_block.get("type") != "sequential":
                    continue

                # subsections
                subsection_usage_key = UsageKey.from_string(subsection_key_str)
                subsection_format = subsection_block.get("format")
                subsections.append(
                    Subsection(
                        id=subsection_usage_key,
                        chapter_id=chapter_usage_key,
                        display_name=subsection_block.get("display_name"),
                        sequence=sequence,
                        format=subsection_format,
                        lms_web_url=subsection_block.get("lms_web_url"),
                        student_view_url=subsection_block.get("student_view_url"),
                        is_special_exam="special_exam_info" in subsection_block,
                        weight=policies.get(subsection_format) or 0,
                    )
                )

                all_children = get_all_children(subsection_key_str)

                for block_key_str in all_children:
                    subsection_child_block = blocks.get(block_key_str)
                    actual_blocks.append(
                        Block(
                            id=UsageKey.from_string(block_key_str),
                            subsection_id=subsection_usage_key,
                            block_type=subsection_child_block.get("type"),
                            display_name=subsection_child_block.get("display_name"),
                            lms_web_url=subsection_child_block.get("lms_web_url"),
                            student_view_url=subsection_child_block.get("student_view_url"),
                        )
                    )

                # library content
                for block_key_str in all_children:
                    subsection_child_block = blocks.get(block_key_str)
                    if subsection_child_block.get("type") == "library_content":
                        library_blocks = cms_client.olx_export_v1_xblock_read(block_key_str)
                        for library_block in library_blocks.get("blocks").keys():
                            usage_key = UsageKey.from_string(library_block)
                            actual_blocks.append(
                                Block(
                                    id=usage_key,
                                    subsection_id=subsection_usage_key,
                                    block_type=usage_key.block_type,
                                    display_name="library content",
                                    lms_web_url="",
                                    student_view_url="",
                                )
                            )

                # next
                sequence += 1

        # create course blocks
        chapters = Chapter.objects.bulk_create(
            chapters,
            update_conflicts=True,
            unique_fields=["id"],
            update_fields=["courserun", "display_name", "sequence"],
        )
        subsections = Subsection.objects.bulk_create(
            subsections,
            update_conflicts=True,
            unique_fields=["id"],
            update_fields=[
                "chapter_id",
                "display_name",
                "sequence",
                "format",
                "lms_web_url",
                "student_view_url",
                "is_special_exam",
                "weight",
            ],
        )
        blocks = Block.objects.bulk_create(
            actual_blocks,
            ignore_conflicts=True,
            unique_fields=["id"],
            update_fields=[
                "subsection_id",
                "block_type",
                "display_name",
                "lms_web_url",
                "student_view_url",
            ],
        )

        # clean
        Chapter.objects.filter(courserun_id=self.id).exclude(
            id__in=[i.id for i in chapters]
        ).delete()
        Subsection.objects.filter(chapter__courserun_id=self.id).exclude(
            id__in=[i.id for i in subsections]
        ).delete()
        Block.objects.filter(subsection__chapter__courserun_id=self.id).exclude(
            id__in=[i.id for i in blocks]
        ).delete()


class CourseDocument(TimeStampedModel):
    class Meta:
        verbose_name = "과정 개요서"
        verbose_name_plural = verbose_name

    # fmt: off

    org = CharField("분류", max_length=20, null=True, blank=True)
    course_document = FileField("과정 개요서", max_length=255, upload_to=upload_to, validators=[FileExtensionValidator(allowed_extensions=["xlsx", "xls"])])
    cover = ImageField("커버 이미지", max_length=255, upload_to=upload_to)
    time_document = FileField("학습 시간 계획서", max_length=255, null=True, blank=True, upload_to=upload_to, validators=[FileExtensionValidator(allowed_extensions=["xlsx", "xls"])])
    content_document = FileField("콘텐츠 경로 문서", max_length=255, null=True, blank=True, upload_to=upload_to, validators=[FileExtensionValidator(allowed_extensions=["xlsx", "xls"])])
    course = OneToOneField("Course", on_delete=SET_NULL, verbose_name="과정", null=True, blank=True)

    # fmt: on

    def __str__(self) -> str:
        return os.path.basename(self.course_document.name)

    @admin_action
    def create_course(self):
        # create Course
        if not self.course:
            course = Course(display_name=EMPTY)
            with self.cover.open("rb") as image_file:
                content = ContentFile(image_file.read())
                name = os.path.basename(self.cover.name)
                course.cover.save(name, content, save=True)

            self.course = course
            self.save()

        org = self.org
        number = self.course.id
        run = getattr(settings, "COURSE_DOCUMENT_RUN_ON", "preview")
        courserun_id = CourseLocator(org=org, course=number, run=run)

        # create preview CourseRun
        CourseRun.objects.get_or_create(
            id=courserun_id,
            # 과정개요서로 생성할 때만 run_number 0부터 시작
            defaults={"course": self.course, "display_name": EMPTY, "run_number": 0},
        )

        # create lms CourseRun
        client = CmsAPIClient()

        start = str(DateUtils.day_start())
        end = str(DateUtils.COURSE_MAX_END)

        try:
            client.v1_course_runs_create(
                {
                    "org": org,
                    "number": number,
                    "run": run,
                    "schedule": {
                        "start": start,
                        "end": end,
                        "enrollment_start": start,
                        "enrollment_end": end,
                    },
                    "pacing_type": "instructor_paced",
                    "team": [],
                    "title": EMPTY,
                }
            )
        except HTTPError:
            # already exists
            pass

        olx = CourseCreator(
            org=org,
            number=number,
            run=run,
            course_document=self.course_document,
            cover=self.cover,
            time_document=self.time_document,
            content_document=self.content_document,
            start=start,
            end=end,
            enrollment_start=start,
            enrollment_end=end,
            certificate_available_date=end,
        ).create_course()

        # upload course tar file
        client.courses_v0_import_create(courserun_id, olx)


class Chapter(Model):
    class Meta:
        verbose_name = "섹션"
        verbose_name_plural = verbose_name
        ordering = ("courserun", "sequence")

    id = UsageKeyField(max_length=255, primary_key=True)
    courserun = ForeignKey(CourseRun, on_delete=CASCADE)
    display_name = CharField(max_length=255)
    sequence = SmallIntegerField(default=0)


class Subsection(Model):
    class Meta:
        verbose_name = "차시"
        verbose_name_plural = verbose_name
        ordering = ("chapter", "sequence")

    id = UsageKeyField(max_length=255, primary_key=True)
    chapter = ForeignKey(Chapter, on_delete=CASCADE)
    display_name = CharField(max_length=255)
    sequence = SmallIntegerField(default=0)
    format = CharField(max_length=50, null=True, blank=True)
    lms_web_url = URLField(max_length=1000)
    student_view_url = URLField(max_length=1000)
    is_special_exam = BooleanField(default=False)
    weight = FloatField(default=0)


class Block(Model):
    class Meta:
        verbose_name = "블록"
        verbose_name_plural = verbose_name

    id = UsageKeyField(max_length=255, primary_key=True)
    subsection = ForeignKey(Subsection, on_delete=CASCADE)
    block_type = CharField(max_length=100, db_index=True)
    display_name = CharField(max_length=255)
    lms_web_url = URLField(max_length=1000)
    student_view_url = URLField(max_length=1000)
