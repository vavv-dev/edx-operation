from django.contrib.auth.models import AbstractUser
from django.db.models import CharField

from .utils.common import random_four_digit


class User(AbstractUser):
    """User."""

    class Meta:
        """Meta."""

        verbose_name = "사용자"
        verbose_name_plural = verbose_name
        get_latest_by = "date_joined"

    full_name = CharField("이름", max_length=255, null=True, blank=True)
    phone_number = CharField("전화번호", max_length=30, null=True, blank=True)
    pin_number = CharField("핀번호", max_length=16, null=True, blank=True, default=random_four_digit)

    @property
    def access_token(self):
        """
        Returns an OAuth2 access token for this user, if one exists; otherwise None.
        Assumes user has authenticated at least once with the OAuth2 provider (LMS).
        """
        try:
            return self.social_auth.first().extra_data["access_token"]  # pylint: disable=no-member
        except Exception:  # pylint: disable=broad-except
            return None

    def get_full_name(self):
        """get_full_name."""
        return self.full_name or super().get_full_name() or self.username

    def __str__(self):
        """__str__."""
        return self.get_full_name()
