from django.db.models import (
    BigIntegerField,
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
)
from django_extensions.db.models import TimeStampedModel

from edx_operation.apps.core.constants import GENDER_CHOICES
from edx_operation.apps.core.utils.common import (
    Validator,
    encrypt_id_number,
    random_four_digit,
)


class Student(TimeStampedModel):
    class Meta:
        verbose_name = "학습자"
        verbose_name_plural = verbose_name

    # fmt: off

    id = CharField("사용자 이름", max_length=100, primary_key=True)
    email = EmailField("이매일", null=True, blank=True)

    name = CharField("이름", max_length=255, null=True, blank=True)
    year_of_birth = CharField("생년월일", max_length=10, null=True, blank=True, validators=[Validator.validate_year_of_birth])
    birthday = CharField("생년월일", max_length=10, null=True, blank=True, validators=[Validator.validate_birthday])
    gender = CharField("성별", max_length=10, null=True, blank=True, choices=GENDER_CHOICES)
    cellphone = CharField("휴대폰", max_length=50, null=True, blank=True, validators=[Validator.validate_cellphone])
    id_number = CharField("주민등록번호", max_length=255, null=True, blank=True)

    initial_password = CharField("패스워드", max_length=100, null=True, blank=True)
    password_change_required = BooleanField("패스워드 변경 안내", default=False)
    pin_number = CharField("핀번호", max_length=16, null=True, blank=True, default=random_four_digit)

    # lms info
    is_active = BooleanField("활성", default=False)
    is_staff = BooleanField("스태프", null=True, blank=True)
    is_superuser = BooleanField("수퍼유저", null=True, blank=True)
    date_joined = DateTimeField("가입", null=True, blank=True)
    last_login = DateTimeField("마지막 로그인", null=True, blank=True)

    # fmt: on

    def set_id_number(self, id_number):
        Validator.validate_id_number(id_number)
        self.id_number = encrypt_id_number(id_number)

    def check_id_number(self, id_number):
        Validator.validate_id_number(id_number)
        return self.id_number == encrypt_id_number(id_number)
