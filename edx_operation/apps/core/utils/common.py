import base64
from datetime import datetime
from datetime import timedelta
import random
import re
import secrets
import string
from uuid import uuid4

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from dateutil import parser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.timezone import localtime

ID_NUMBER_ENCRYPTION_KEY = getattr(settings, "ID_NUMBER_ENCRYPTION_KEY", b"secureencryption")


def random_color():
    """random_color."""
    rand = lambda: random.randint(100, 255)
    return "#%02X%02X%02X" % (rand(), rand(), rand())


def secure_redeem_code(length=8):
    characters = string.ascii_uppercase + string.digits
    code = "".join(secrets.choice(characters) for _ in range(length))
    return code


def random_four_digit():
    return str(random.randint(1000, 9999))


def upload_unique_name(instance, filename, *args, **kwargs):
    class_name = instance.__class__.__name__
    dirname = re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).lower()
    return "{0}/{2}.{1}.{3}".format(dirname, uuid4().hex[:8], *filename.rsplit(".", 1))


class DateUtils:
    COURSE_MAX_END = parser.isoparse("2049-12-31 23:59:59+09:00")

    @staticmethod
    def day_start(time=None):
        return (time or localtime()).replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def day_end(time=None):
        return DateUtils.day_start(time) + timedelta(days=1, seconds=-1)


class Validator:
    @staticmethod
    def validate_id_number(value: str):
        pattern = re.compile(r"^\d{6}-\d{7}$")
        if not pattern.match(value):
            raise ValidationError("주민등록번호의 형식이 올바르지 않습니다.")

    @staticmethod
    def validate_cellphone(value: str):
        if not re.match(r"^\d{3}-\d{3,4}-\d{3,4}$", value):
            raise ValidationError("휴대폰 번호 형식이 올바르지 않습니다.")

    @staticmethod
    def validate_year_of_birth(value: str):
        if not (value.isdigit() and len(value) == 4):
            raise ValidationError("출생 연도는 네 자리 숫자여야 합니다.")

        current_year = datetime.now().year
        if not (1900 <= int(value) <= current_year):
            raise ValidationError("유효하지 않은 출생 연도입니다.")

    @staticmethod
    def validate_birthday(value: str):
        try:
            datetime.strptime(value, "%m%d")
        except ValueError:
            raise ValidationError("유효하지 않은 생일 형식입니다.")

    @staticmethod
    def validate_esimsa_code(value: str):
        pattern = re.compile(r"^\w\d{8}\d{4}\w\d\d\d{2}\d{2}$")
        if not pattern.match(value):
            raise ValidationError("코드 형식이 올바르지 않습니다.")

    @staticmethod
    def validate_hrd_net_code(value: str):
        if len(value) != 17:
            raise ValidationError("코드 형식이 올바르지 않습니다.")


def encrypt_id_number(id_number):
    id_number = id_number.replace("-", "")
    key = ID_NUMBER_ENCRYPTION_KEY
    obj = AES.new(key, AES.MODE_ECB)
    padded_data = pad(bytes(id_number, "utf-8"), 16)
    encrypted_data = obj.encrypt(padded_data)
    return base64.b64encode(encrypted_data).decode("utf-8")


def decrypt_id_number(encrypted_base64):
    # cf Mysql: aes_decrypt(from_base64(id_number), 'key')
    encrypted_data = base64.b64decode(encrypted_base64.encode("utf-8"))
    key = ID_NUMBER_ENCRYPTION_KEY
    obj = AES.new(key, AES.MODE_ECB)
    decrypted_data = obj.decrypt(encrypted_data)
    id_number = unpad(decrypted_data, 16)
    id_number = id_number.decode("utf-8")
    return f"{id_number[:6]}-{id_number[6:]}"


def admin_action(func):
    setattr(func, "_admin_action", True)
    return func


def paginate(objs, page, per_page):
    paginator = Paginator(objs, per_page)
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)

    setattr(
        paginator,
        "elided_page_range",
        paginator.get_elided_page_range(objs.number, on_each_side=3, on_ends=1),
    )

    # numbering
    setattr(
        paginator,
        "base_no",
        (paginator.count or 0) - int(per_page) * (objs.number - 1) - len(objs.object_list),
    )
    return objs
