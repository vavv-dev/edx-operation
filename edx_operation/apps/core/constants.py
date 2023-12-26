""" Constants for the core app. """


class Status:
    """Health statuses."""

    OK = "OK"
    UNAVAILABLE = "UNAVAILABLE"


# 과정 생성 중을 나타내는 임시 제목
EMPTY_COURSE_DISPLAY_NAME = "empty"

# gender
GENDER_CHOICES = (
    ("f", "여성"),
    ("m", "남성"),
    ("o", "기타"),
)

# tutor perm codename
TUTOR_PERM = "tutor"

# marketer perm codename
MARKETER_PERM = "marketer"

# course accredit perm codename
COURSEACCREDIT_PERM = "accredit_manager"

# program
FIXED_SCHEDULE = "fixed_schedule"
INDIVIDUAL_SCHEDULE = "individual_schedule"
