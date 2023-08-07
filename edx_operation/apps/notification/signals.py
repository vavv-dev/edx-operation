from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify

from edx_operation.apps.enrollment.models import Enrollment
from edx_operation.apps.student.models import Student


@receiver(post_save, sender=Student)
def student_post_save(sender, instance, created, **kwargs):
    # registratino
    if created:
        notify.send(
            instance,
            recipient=instance,
            verb="was registered",
        )


@receiver(post_save, sender=Enrollment)
def enrollment_post_save(sender, instance, created, **kwargs):
    # course enrollment
    if created:
        notify.send(
            instance,
            recipient=instance.student,
            verb="was enrolled",
            action_object=instance,
            target=instance.course,
        )
