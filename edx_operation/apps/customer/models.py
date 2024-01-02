from django.db.models import (
    CASCADE,
    CharField,
    EmailField,
    ForeignKey,
    ImageField,
    ManyToManyField,
    SlugField,
)
from django.db.models.fields import BooleanField
from django_extensions.db.models import TimeStampedModel
from wagtail.search.index import AutocompleteField, Indexed, SearchField
from wagtail.snippets.models import register_snippet

from edx_operation.apps.core.utils.common import random_four_digit
from edx_operation.apps.enrollment.models import Enrollment
from edx_operation.apps.student.models import Student


class Customer(TimeStampedModel, Indexed):
    class Meta:
        verbose_name = "고객사"
        verbose_name_plural = verbose_name

    # fmt: off

    name = CharField("고객사", max_length=255, db_index=True)
    slug = SlugField("슬러그", max_length=255, unique=True)
    logo = ImageField("로고", max_length=255, null=True, blank=True)
    email = EmailField("이메일", null=True, blank=True)
    size = CharField("규모", max_length=255, null=True, blank=True)
    phone = CharField("전화", max_length=50, null=True, blank=True)
    fax = CharField("팩스", max_length=50, null=True, blank=True)

    ceo_name = CharField("CEO", max_length=50, null=True, blank=True)
    postal_code = CharField("우편번호", max_length=10, null=True, blank=True)
    business_registration_number = CharField("사업자등록번호", max_length=50, null=True, blank=True, db_index=True)
    business_management_number = CharField("사업장관리번호", max_length=50, null=True, blank=True, db_index=True)
    address = CharField("주소", max_length=254, null=True, blank=True)
    pin_number = CharField("핀번호", max_length=16, null=True, blank=True, default=random_four_digit)
    students = ManyToManyField(Student, through="CustomerStudent", blank=True, verbose_name="학습자")
    enrollments = ManyToManyField(Enrollment, through="CustomerEnrollment", blank=True, verbose_name="수강")

    # fmt: on

    search_fields = (
        SearchField("name"),
        AutocompleteField("name"),
    )

    def __str__(self) -> str:
        return self.name


class CustomerStudent(TimeStampedModel):
    class Meta:
        verbose_name = "고객사 학습자"
        verbose_name_plural = verbose_name
        unique_together = (("customer", "student"),)

    # fmt: off

    customer = ForeignKey(Customer, on_delete=CASCADE, verbose_name="고객사")
    student = ForeignKey(Student, on_delete=CASCADE, verbose_name="학습자")
    is_active = BooleanField("활성", default=True)
    department = CharField("부서", max_length=100, null=True, blank=True)
    job_title = CharField("직위", max_length=100, null=True, blank=True)
    job_responsibility = CharField("직책", max_length=100, null=True, blank=True)
    occupation_type = CharField("고용 형태", max_length=10, null=True, blank=True)
    working_type = CharField("근로 형태", max_length=10, null=True, blank=True)

    # fmt: on


class CustomerEnrollment(TimeStampedModel):
    class Meta:
        verbose_name = "고객사 수강"
        verbose_name_plural = verbose_name
        unique_together = (("customer", "enrollment"),)

    # fmt: off

    customer = ForeignKey(Customer, on_delete=CASCADE, verbose_name="고객사")
    enrollment = ForeignKey(Enrollment, on_delete=CASCADE, verbose_name="수강")
    is_active = BooleanField("활성", default=True)

    # fmt: on
