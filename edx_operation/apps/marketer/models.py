from django.contrib.auth.models import Permission, UserManager
from django.db.models import (
    BooleanField,
    CASCADE,
    FileField,
    ForeignKey,
    ManyToManyField,
    OneToOneField,
)
from django_extensions.db.models import TimeStampedModel

from edx_operation.apps.core.constants import MARKETER_PERM
from edx_operation.apps.core.models import User
from edx_operation.apps.core.utils.common import upload_unique_name
from edx_operation.apps.course.models import Course, CourseRun
from edx_operation.apps.customer.models import Customer


class MarketerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user_permissions__codename=MARKETER_PERM)


class Marketer(User):
    class Meta:
        proxy = True
        verbose_name = "영업자"
        verbose_name_plural = verbose_name
        permissions = ((MARKETER_PERM, "영업자"),)

    # change default manager
    objects = MarketerManager()
    user_objects = UserManager()

    def save(self, *args, **kwargs):
        to_create = not self.pk
        super().save(*args, **kwargs)

        if to_create:
            marketer_perm = Permission.objects.get(codename=MARKETER_PERM)
            self.user_permissions.add(marketer_perm)


class MarketerInfo(TimeStampedModel):
    class Meta:
        verbose_name = "영업자 정보"
        verbose_name_plural = verbose_name

    # fmt: off

    marketer = OneToOneField(Marketer, on_delete=CASCADE, verbose_name="영업자")
    is_active = BooleanField("활성", default=True)
    # TODO pin_number protection
    contract = FileField("계약서", null=True, blank=True, upload_to=upload_unique_name)
    customers = ManyToManyField(Customer, through="CustomerManaging", verbose_name="담당 고객사", blank=True)
    courseruns = ManyToManyField(CourseRun, through="CourseRunManaging", verbose_name="담당 회차", blank=True)

    # fmt: on


class CustomerManaging(TimeStampedModel):
    class Meta:
        verbose_name = "담당 고객사"
        verbose_name_plural = verbose_name

    marketerinfo = ForeignKey(MarketerInfo, on_delete=CASCADE, verbose_name="영업자")
    customer = OneToOneField(Customer, on_delete=CASCADE, verbose_name="고객사")


class CourseRunManaging(TimeStampedModel):
    class Meta:
        verbose_name = "담당 회차"
        verbose_name_plural = verbose_name

    marketerinfo = ForeignKey(MarketerInfo, on_delete=CASCADE, verbose_name="영업자")
    courserun = OneToOneField(CourseRun, on_delete=CASCADE, verbose_name="회차")
