from django.db import models
from django.utils.translation import gettext_lazy as _
from notifications.base.models import AbstractNotification


class StudentNotification(AbstractNotification):
    class Meta(AbstractNotification.Meta):
        abstract = False
        verbose_name = _("Student Notification")
        verbose_name_plural = _("Student Notifications")

    recipient = models.ForeignKey(
        "student.Student",
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("recipient"),
        blank=False,
    )

    # override
    public = models.BooleanField(_("public"), default=False, db_index=True)
