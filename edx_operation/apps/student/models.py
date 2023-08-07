from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from edx_operation.apps.api_client.jwt import LmsAPIClient


class Student(TimeStampedModel):
    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    GENDER_CHOICES = (("f", "여성"), ("m", "남성"))

    username = models.CharField(max_length=100, null=True, blank=True, unique=True)
    email = models.EmailField(null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True)
    is_staff = models.BooleanField(null=True, blank=True)
    is_superuser = models.BooleanField(null=True, blank=True)
    date_joined = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)

    name = models.CharField(max_length=255, null=True, blank=True)
    id_number = models.CharField(max_length=255, null=True, blank=True)
    year_of_birth = models.CharField(max_length=10, null=True, blank=True)
    birthday = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=GENDER_CHOICES)
    cellphone = models.CharField(max_length=50, null=True, blank=True)

    @property
    def decrypted_id_number(self):
        return settings.cipher_suite.decrypt(self.id_number).decode()

    @property
    def initial_password(self):
        password = InitialPassword.objects.filter(username=self.username).last()
        return password.password if password else None

    def set_id_number(self, id_number):
        self.id_number = settings.cipher_suite.encrypt(id_number.encode())

    def check_id_number(self, id_number):
        return self.decrypted_id_number == id_number

    @classmethod
    def register(cls, name, username, email, year_of_birth, initial_password):
        payload = {
            "name": name,
            "username": username,
            "email": email,
            "year_of_birth": year_of_birth,
            "password": initial_password,
            "country": "KR",
            "honor_code": True,
        }

        # create user
        LmsAPIClient().user_v1_account_registration_create(payload)

        # save initial_password
        InitialPassword.objects.update_or_create(
            username=username,
            defaults={"password": initial_password},
        )


class InitialPassword(TimeStampedModel):
    class Meta:
        verbose_name = _("Initial Password")
        verbose_name_plural = _("Initial Passwords")

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
