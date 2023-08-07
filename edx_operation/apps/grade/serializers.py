from rest_framework import serializers

from edx_operation.apps.grade.models import CourseGrade


class CourseSerializerField(serializers.Field):
    def to_representation(self, value):
        return str(value.id)


class CourseGradeSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name="v1:coursegrade-detail")
    course = CourseSerializerField(read_only=True)

    class Meta:
        model = CourseGrade
        fields = "__all__"
