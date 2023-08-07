import random

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from edx_operation.apps.api_client.jwt import EnterpriseAPIClient


def random_digits():
    return str(random.randint(1000, 9999))


class Site(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    domain = models.CharField(max_length=255, unique=True)


class Partner(TimeStampedModel):
    class Meta:
        verbose_name = _("Partner Customer")
        verbose_name_plural = _("Partner Customers")

    SIZE_CHOICES = (("large", "대기업"), ("middle", "중견기업"), ("small", "우선지원기업"))

    uuid = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=30, unique=True)
    active = models.BooleanField(null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)

    size = models.CharField(max_length=255, null=True, blank=True, choices=SIZE_CHOICES)
    phone = models.CharField(max_length=50, null=True, blank=True, help_text="ex) 02-1234-1234")
    fax = models.CharField(max_length=50, null=True, blank=True, help_text="ex) 02-1234-1234")
    management_number = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    id_number = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    ceo_name = models.CharField(max_length=50, null=True, blank=True, help_text="ex) 홍길동")
    postal_code = models.CharField(max_length=10, null=True, blank=True, help_text="ex) 12345")
    address = models.CharField(max_length=254, null=True, blank=True, help_text="ex) 서울시 서초구...")
    secondary_key = models.CharField(max_length=16, null=True, blank=True, default=random_digits)
    students = models.ManyToManyField("student.Student", through="partner.PartnerStudent")

    @classmethod
    def join(cls, name: str, slug: str, domain: str):
        if cls.objects.filter(Q(name=name) | Q(slug=slug)):
            raise ValueError("Name or slug already exists.")

        client = EnterpriseAPIClient()

        # partner customer
        customer = client.v1_enterprise_customer_create(
            {
                "name": name,
                "slug": slug,
                "active": True,
                "site": {"domain": domain},
                "enable_learner_portal": True,
                "enable_data_sharing_consent": True,
                "enable_portal_code_management_screen": True,
                "enable_portal_reporting_config_screen": True,
                "enable_portal_saml_configuration_screen": True,
                "enable_portal_subscription_management_screen": True,
                "enable_portal_lms_configurations_screen": True,
            }
        )

        # enterprise customer catalog
        client.v1_enterprise_customer_catalog_create(
            {
                "title": name,
                "enterprise_customer": customer.get("uuid"),
            }
        )


class PartnerStudent(TimeStampedModel):
    class Meta:
        verbose_name = _("Partner Student")
        verbose_name_plural = _("Partner Students")
        unique_together = (("partner", "student"),)

    partner = models.ForeignKey("partner.Partner", on_delete=models.deletion.CASCADE)
    student = models.ForeignKey("student.Student", on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    linked = models.BooleanField(default=True)

    @classmethod
    def link(cls, username, partner_id):
        EnterpriseAPIClient().v1_enterprise_learner_create(
            {
                "enterprise_customer": str(partner_id),
                "username": username,
                "active": True,
            }
        )


class PartnerEnrollment(TimeStampedModel):
    class Meta:
        verbose_name = _("Partner Enrollment")
        verbose_name_plural = _("Partner Enrollments")
        unique_together = (("partner_student", "course"),)

    partner_student = models.ForeignKey("partner.PartnerStudent", on_delete=models.CASCADE)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE)
    saved_for_later = models.BooleanField(null=True, blank=True)
    unenrolled = models.BooleanField(null=True, blank=True, db_index=True)
    unenrolled_at = models.DateTimeField(null=True, blank=True)

    @classmethod
    def enroll(cls, username, course_id):
        payload = {
            "username": username,
            "course_id": str(course_id),
        }

        EnterpriseAPIClient().v1_enterprise_course_enrollment_create(payload)
