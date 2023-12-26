from datetime import datetime

from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    OneToOneField,
)
from django.utils.timezone import make_aware
from django_extensions.db.models import TimeStampedModel

from edx_operation.apps.core.constants import COURSEACCREDIT_PERM
from edx_operation.apps.core.utils.common import Validator, admin_action
from edx_operation.apps.course.models import Course, CourseRun


class CourseAccredit(TimeStampedModel):
    class Meta:
        verbose_name = "과정 승인"
        verbose_name_plural = verbose_name
        permissions = ((COURSEACCREDIT_PERM, "과정 승인 담당자"),)

    # fmt: off

    course = OneToOneField(Course, on_delete=CASCADE, verbose_name="과정")
    courserun = ForeignKey(CourseRun, on_delete=CASCADE, verbose_name="회차")
    esimsa_code = CharField("과정 승인 코드", max_length=50, null=True, blank=True, validators=[Validator.validate_esimsa_code])
    esimsa_code_expiration = DateTimeField("과정 승인 만료", null=True, blank=True)

    # fmt: on

    def add_tester(self, users):
        # TODO
        pass

    @admin_action
    def notify_to_managers(self):
        # TODO
        pass

    @property
    def training_type(self):
        """훈련 유형"""

        if not self.esimsa_code:
            return

        code = self.esimsa_code.replace("-", "")[0:1].upper()

        if code == "I":
            return "인터넷원격"
        elif code == "P":
            return "우편원격"
        elif code == "U":
            return "기업대학"
        elif code == "C":
            return "콘소시엄"
        elif code == "H":
            return "스마트훈련"
        elif code == "B":
            return "혼합훈련"
        elif code == "N":
            return "실업자원격"
        elif code == "D":
            return "디지털융합"

    @property
    def content_start_date(self):
        """심사 발급 일자"""

        if not self.esimsa_code:
            return

        code = self.esimsa_code.replace("-", "")[1:9]

        try:
            return make_aware(datetime.strptime(code, "%Y%m%d"))
        except:
            return None

    @property
    def is_postal_course(self):
        """우편 과정"""
        return True if self.training_type == "P" else False

    @property
    def content_category(self):
        """심사 유형"""

        if not self.esimsa_code:
            return

        code = self.esimsa_code.replace("-", "")[13:14]

        if code == "L":
            return "전문직무"
        elif code == "F":
            return "외국어"
        elif code == "A":
            return "NCS 적용 과정"
        elif code == "R":
            return "법정직무과정"
        elif code == "C":
            return "공통법정"
        elif code == "D":
            return "직무법정"
        elif code == "J":
            return "공통직무"

    @property
    def supply_level(self):
        """공급 정도"""

        if not self.esimsa_code:
            return

        level = self.esimsa_code.replace("-", "")[14:15]

        if level == "1":
            return 0.7
        elif level == "2":
            return 0.8
        elif level == "3":
            return 0.9
        elif level == "4":
            return 1.0

    @property
    def content_grade(self):
        """과정 코드 심사 등급"""

        if not self.esimsa_code:
            return

        code = self.esimsa_code.replace("-", "")[15:16]

        if code == "1":
            return "A등급"
        elif code == "2":
            return "B등급"
        elif code == "3":
            return "C등급"
        else:
            return

    @property
    def training_hours(self):
        """훈련 시간"""

        if not self.esimsa_code:
            return

        return self.esimsa_code.replace("-", "")[16:18]
