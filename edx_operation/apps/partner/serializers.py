from rest_framework import serializers
from edx_operation.apps.course.models import Course

from edx_operation.apps.partner.models import (
    Partner,
    PartnerEnrollment,
    PartnerStudent,
    Site,
)


class PartnerSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name="v1:partner-detail")

    class Meta:
        model = Partner
        fields = "__all__"


class PartnerCSerializer(serializers.ModelSerializer):
    domain = serializers.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        domains = Site.objects.values_list("domain", "name")
        self.fields["domain"].choices = domains

    class Meta:
        model = Partner
        fields = ("name", "slug", "domain")


class PartnerStudentSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name="v1:partnerstudent-detail")

    class Meta:
        model = PartnerStudent
        fields = "__all__"


class PartnerStudentCSerializer(serializers.ModelSerializer):
    partner_id = serializers.ChoiceField(choices=[])
    username = serializers.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # partner
        partner_ids = [
            (str(uuid), f"{name} / {uuid}")
            for uuid, name in Partner.objects.values_list("uuid", "name")
        ]
        self.fields["partner_id"].choices = partner_ids

    class Meta:
        model = PartnerStudent
        fields = ("partner_id", "username")


class CourseSerializerField(serializers.Field):
    def to_representation(self, value):
        return str(value.id)


class PartnerEnrollmentSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name="v1:partnerenrollment-detail")
    course = CourseSerializerField(read_only=True)

    class Meta:
        model = PartnerEnrollment
        fields = "__all__"


class PartnerEnrollmentCSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    course_id = serializers.ChoiceField([])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # course
        course_ids = [
            (str(id), f"{display_name} / {id}")
            for id, display_name in Course.objects.values_list("id", "display_name")
        ]
        self.fields["course_id"].choices = course_ids

    class Meta:
        model = PartnerEnrollment
        fields = ("username", "course_id")
