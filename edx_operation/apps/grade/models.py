from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from opaque_keys.edx.django.models import UsageKeyField
from simple_history.models import HistoricalRecords


class CourseGrade(TimeStampedModel):
    class Meta:
        unique_together = (("student", "course"),)

    student = models.ForeignKey("student.Student", on_delete=models.CASCADE)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE)
    percent_grade = models.FloatField(null=True, blank=True)
    letter_grade = models.CharField(max_length=255, null=True, blank=True)
    passed = models.BooleanField(null=True, blank=True)
    grade_summary = models.JSONField(null=True, blank=True)

    # history
    history = HistoricalRecords()


class SubsectionGrade(TimeStampedModel):
    class Meta:
        unique_together = (("student", "usage_key"),)

    student = models.ForeignKey("student.Student", on_delete=models.CASCADE)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE)
    usage_key = UsageKeyField(max_length=255)
    earned_all = models.FloatField(null=True, blank=True)
    possible_all = models.FloatField(null=True, blank=True)
    earned_graded = models.FloatField(null=True, blank=True)
    possible_graded = models.FloatField(null=True, blank=True)
    due = models.DateTimeField(null=True, blank=True)
    complete = models.BooleanField(null=True, blank=True)
    completion_block = UsageKeyField(max_length=255, null=True, blank=True)
    client_ip = models.CharField(max_length=50, null=True, blank=True)

    # history
    history = HistoricalRecords()


class ExamStatus(TimeStampedModel):
    class Meta:
        unique_together = (("student", "usage_key"),)

    student = models.ForeignKey("student.Student", on_delete=models.CASCADE)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE)
    usage_key = UsageKeyField(max_length=255)
    is_active = models.BooleanField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    deleted = models.BooleanField(null=True, blank=True)


class Submission(TimeStampedModel):
    uuid = models.UUIDField(unique=True)
    student = models.ForeignKey("student.Student", on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE, null=True, blank=True)
    usage_key = UsageKeyField(max_length=255, null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10, null=True, blank=True, choices=(("D", "Deleted"), ("A", "Active"))
    )
    score = models.FloatField(null=True, blank=True)
    scored_at = models.DateTimeField(null=True, blank=True)
    score_reset = models.BooleanField(null=True, blank=True)
