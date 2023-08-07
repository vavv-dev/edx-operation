from django.dispatch import receiver

from edx_operation.apps.event.kafka import OPERATION_EVENT_SIGNAL
from edx_operation.apps.partner.models import Partner, PartnerEnrollment, PartnerStudent, Site


@receiver(OPERATION_EVENT_SIGNAL)
def log_operation_event(event, **kwargs):
    if event.event_type == "operation_event.signals.enterprisecustomeruser":
        m = event.message
        PartnerStudent.objects.update_or_create(
            id=m.get("id"),
            defaults={
                "created": m.get("created"),
                "modified": m.get("modified"),
                "partner_id": m.get("enterprise_customer_id"),
                "student_id": m.get("user_id"),
                "active": m.get("active"),
                "linked": m.get("linked"),
            },
        )

    elif event.event_type == "operation_event.signals.enterprisecourseenrollment":
        m = event.message
        PartnerEnrollment.objects.update_or_create(
            id=m.get("id"),
            defaults={
                "created": m.get("created"),
                "modified": m.get("modified"),
                "partner_student_id": m.get("enterprise_customer_user_id"),
                "course_id": m.get("course_id"),
                "saved_for_later": m.get("saved_for_later"),
                "unenrolled": m.get("unenrolled"),
                "unenrolled_at": m.get("unenrolled_at"),
            },
        )

    elif event.event_type == "operation_event.signals.enterprisecustomer":
        m = event.message
        Partner.objects.update_or_create(
            uuid=m.get("uuid"),
            defaults={
                "created": m.get("created"),
                "modified": m.get("modified"),
                "name": m.get("name"),
                "slug": m.get("slug"),
                "active": m.get("active"),
                "site_id": m.get("site_id"),
            },
        )

    elif event.event_type == "operation_event.signals.site":
        m = event.message
        Site.objects.update_or_create(
            id=m.get("id"),
            defaults={
                "name": m.get("name"),
                "domain": m.get("domain"),
            },
        )
