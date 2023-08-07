from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from edx_operation.apps.course.models import Course
from edx_operation.apps.enrollment.models import Enrollment


class CourseSerializerField(serializers.Field):
    def to_representation(self, value):
        return str(value.id)


class EnrollmentSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name="v1:enrollment-detail")
    course = CourseSerializerField(read_only=True)

    class Meta:
        model = Enrollment
        fields = "__all__"


class EnrollmentCSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    course_id = serializers.ChoiceField([])
    mode = serializers.ChoiceField(
        [
            ("audit", _("audit")),
            ("honor", _("honor")),
            ("verified", _("verified")),
            ("professional", _("professional")),
        ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # course choices
        course_ids = [
            (str(id), f"{display_name} / {id}")
            for id, display_name in Course.objects.values_list("id", "display_name")
        ]
        self.fields["course_id"].choices = course_ids

    class Meta:
        model = Enrollment
        fields = (
            "username",
            "course_id",
            "mode",
        )
