from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    id = models.CharField(max_length=50, primary_key=True, editable=False)
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    annoymous = models.BooleanField(null=True, blank=True)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE)
    thread = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="comments"
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    depth = models.SmallIntegerField(null=True, blank=True)
    commentable_id = models.CharField(max_length=255)
    student = models.ForeignKey("student.Student", on_delete=models.CASCADE)
    thread_type = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    closed = models.BooleanField(null=True, blank=True)
    votes = models.JSONField(null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    deleted = models.BooleanField(null=True, blank=True)
