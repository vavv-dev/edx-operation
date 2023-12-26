from django.contrib.auth.models import Permission, UserManager
from django.db.models import (
    BooleanField,
    CASCADE,
    ForeignKey,
    GenericIPAddressField,
    ImageField,
    ManyToManyField,
    OneToOneField,
    TextField,
)
from django_extensions.db.models import TimeStampedModel

from edx_operation.apps.core.constants import TUTOR_PERM
from edx_operation.apps.core.models import User
from edx_operation.apps.core.utils.common import upload_unique_name
from edx_operation.apps.enrollment.models import Enrollment
from edx_operation.apps.grade.models import Submission
from edx_operation.apps.student.models import Student


class TutorManager(UserManager):
    """TutorManager."""

    def get_queryset(self):
        """get_queryset."""
        return super().get_queryset().filter(user_permissions__codename=TUTOR_PERM)


class Tutor(User):
    """Tutor."""

    class Meta:
        """Meta."""

        proxy = True
        verbose_name = "튜터"
        verbose_name_plural = verbose_name
        permissions = ((TUTOR_PERM, "튜터"),)

    # change default manager
    objects = TutorManager()
    user_objects = UserManager()

    def save(self, *args, **kwargs):
        """save.

        :param args:
        :param kwargs:
        """
        to_create = not self.pk
        super().save(*args, **kwargs)

        if to_create:
            tutor_perm = Permission.objects.get(codename=TUTOR_PERM)
            self.user_permissions.add(tutor_perm)


class TutorInfo(TimeStampedModel):
    """TutorInfo."""

    class Meta:
        """Meta."""

        verbose_name = "튜터 정보"
        verbose_name_plural = verbose_name

    # fmt: off

    tutor = OneToOneField(Tutor, on_delete=CASCADE, verbose_name="튜터")
    is_active = BooleanField("활성", default=True)
    avatar = ImageField("이미지", upload_to=upload_unique_name, null=True, blank=True)
    bio = TextField("학력/경력", null=True, blank=True)
    enrollments = ManyToManyField(Enrollment, through="Tutoring", verbose_name="담당 수강", blank=True)
    scorings = ManyToManyField(Submission, through="Scoring", verbose_name="담당 채점", blank=True)

    # fmt: on


class Tutoring(TimeStampedModel):
    """Tutoring."""

    class Meta:
        """Meta."""

        verbose_name = "튜터링"
        verbose_name_plural = verbose_name

    tutorinfo = ForeignKey(TutorInfo, on_delete=CASCADE, verbose_name="튜터")
    enrollment = OneToOneField(Enrollment, on_delete=CASCADE, verbose_name="수강")


class Scoring(TimeStampedModel):
    """Scoring."""

    class Meta:
        """Meta."""

        verbose_name = "채점"
        verbose_name_plural = verbose_name

    tutorinfo = ForeignKey(TutorInfo, on_delete=CASCADE, verbose_name="튜터")
    submission = OneToOneField(Submission, on_delete=CASCADE, verbose_name="제출")
    client_ip = GenericIPAddressField("IP 주소", null=True, blank=True)
