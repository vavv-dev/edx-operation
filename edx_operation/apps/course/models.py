import logging
import random
import string

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from opaque_keys.edx.django.models import CourseKeyField, UsageKeyField
from opaque_keys.edx.keys import UsageKey

from edx_operation.apps.api_client.jwt import CmsAPIClient, LmsAPIClient
from edx_operation.apps.api_client.session import LmsAPIClient as SessionClient

log = logging.getLogger("__name__")


class Course(TimeStampedModel):
    class Meta:
        unique_together = ("org", "number", "run")

    id = CourseKeyField(max_length=255, primary_key=True)
    org = models.CharField(max_length=255, db_index=True, editable=False)
    number = models.CharField(max_length=255, db_index=True, editable=False)
    run = models.CharField(max_length=255, db_index=True, editable=False)
    display_name = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    invitation_only = models.BooleanField(null=True, blank=True)
    course_image_url = models.URLField(max_length=1000, null=True, blank=True)
    effort = models.CharField(max_length=20, null=True, blank=True)
    visible_to_staff_only = models.BooleanField(null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    enrollment_start = models.DateTimeField(null=True, blank=True)
    enrollment_end = models.DateTimeField(null=True, blank=True)
    certificate_available_date = models.DateTimeField(null=True, blank=True)
    pacing = models.CharField(max_length=50, null=True, blank=True)

    @classmethod
    def import_olx(cls, title, org, olx):
        start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + relativedelta(months=2, minutes=-1)

        # create course run
        client = CmsAPIClient()

        # create new course
        course = client.v1_course_runs_create(
            {
                "org": org,
                "number": cls.random_number(),
                "run": cls.random_run(),
                "schedule": {
                    "start": str(start),
                    "end": str(end),
                    "enrollment_start": str(start),
                    "enrollment_end": str(end),
                },
                "pacing_type": "instructor_paced",
                "team": [],
                "title": title,
            }
        )

        # upload course tar file
        client.courses_v0_import_create(course.get("id"), olx)

    @classmethod
    def rerun(cls, source_course_id, start, end, title_override=None):
        source_course = cls.objects.get(id=source_course_id)

        if not title_override:
            title_override = source_course.display_name

        # cf. cms/djangoapps/contentstore/views/course.py:1060
        # enrollment_start, enrollment_end not working

        # api client
        CmsAPIClient().v1_course_runs_rerun(
            source_course.id,
            {
                "run": cls.random_run(),
                "title": title_override,
                "pacing_type": f"{source_course.pacing}_paced",
                "schedule": {
                    "start": str(start),
                    "end": str(end),
                    "enrollment_start": str(start),
                    "enrollment_end": str(end),
                },
            },
        )

    @classmethod
    def random_number(cls):
        number = None
        while True:
            number = "".join(random.choice(string.ascii_lowercase) for _ in range(8))
            if not cls.objects.filter(number=number).exists():
                break
        return number

    @classmethod
    def random_run(cls):
        run = None
        while True:
            random_code = "".join(random.choices(string.ascii_uppercase, k=3))
            run = localtime().strftime("%Y%m%d") + random_code
            if not cls.objects.filter(run=run).exists():
                break
        return run

    def create_course_modes(self, course_modes=None):
        course_id = str(self.id)

        if not course_modes:
            course_modes = [
                {
                    "course_id": course_id,
                    **mode,
                }
                for mode in settings.COURSE_MODES
            ]

        # create course mode
        LmsAPIClient().course_modes_v1_curses_create(course_id, course_modes)

    def sync_course_blocks(self):
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

        blocks = course_blocks.get("blocks")
        course_block = blocks.get(course_blocks.get("root"))

        # subsection sequence
        sequence = 1

        # subsection's all children
        def get_all_children(block):
            if "children" not in blocks[block]:
                return set()

            children = blocks[block]["children"]
            all_children = set(children)

            for child in children:
                all_children.update(get_all_children(child))

            return all_children

        # inactivate all blocks
        Block.objects.filter(subsection__chapter__course=self).delete()
        Subsection.objects.filter(chapter__course=self).delete()
        Chapter.objects.filter(course=self).delete()

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
                    usage_key=chapter_usage_key,
                    course_id=self.id,
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
                        usage_key=subsection_usage_key,
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
                            usage_key=UsageKey.from_string(block_key_str),
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
                                    usage_key=usage_key,
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
        Chapter.objects.bulk_create(chapters, ignore_conflicts=True)
        Subsection.objects.bulk_create(subsections, ignore_conflicts=True)
        Block.objects.bulk_create(actual_blocks, ignore_conflicts=True)


class Chapter(models.Model):
    class Meta:
        ordering = ("course", "sequence")

    usage_key = UsageKeyField(max_length=255, primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255)
    sequence = models.SmallIntegerField(default=0)


class Subsection(models.Model):
    class Meta:
        ordering = ("chapter", "sequence")

    usage_key = UsageKeyField(max_length=255, primary_key=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255)
    sequence = models.SmallIntegerField(default=0)
    format = models.CharField(max_length=50, null=True, blank=True)
    lms_web_url = models.URLField(max_length=1000)
    student_view_url = models.URLField(max_length=1000)
    is_special_exam = models.BooleanField(default=False)
    weight = models.FloatField(default=0)


class Block(models.Model):
    usage_key = UsageKeyField(max_length=255, primary_key=True)
    subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE)
    block_type = models.CharField(max_length=100, db_index=True)
    display_name = models.CharField(max_length=255)
    lms_web_url = models.URLField(max_length=1000)
    student_view_url = models.URLField(max_length=1000)


class CourseAccessRole(TimeStampedModel):
    class Meta:
        unique_together = ("student", "org", "course_id", "role")

    student = models.ForeignKey("student.Student", on_delete=models.CASCADE)
    org = models.CharField(max_length=64, db_index=True, null=True, blank=True)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=64, db_index=True)
    deleted = models.BooleanField(null=True, blank=True)

    @classmethod
    def allow(cls, request, username, course_id, role):
        """
        add CourseAccessRole

        :param cls CourseAccessRole:
        :param request Request: request from browser with cookies
        :param username str:
        :param course_id CourseKey:
        :param role str: ["instructor", "staff", "beta"]
        """

        cookies = request.COOKIES
        headers = {"X-CSRFToken": cookies["csrftoken"]}

        SessionClient(headers=headers, cookies=cookies).modyfy_access_create(
            course_id,
            data={
                "unique_student_identifier": username,
                "rolename": role,
                "action": "allow",
            },
        )
