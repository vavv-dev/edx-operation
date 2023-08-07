from rest_framework import serializers

from edx_operation.apps.course.models import Course, CourseAccessRole


class CourseSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name="v1:course-detail")

    class Meta:
        model = Course
        fields = "__all__"


class CourseISerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50)
    org = serializers.CharField(max_length=50)
    olx = serializers.FileField()

    class Meta:
        model = Course
        fields = ("title", "org", "olx")


class CourseCSerializer(serializers.ModelSerializer):
    source_course_id = serializers.ChoiceField([])
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    title_override = serializers.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # source course choices
        course_ids = [
            (str(id), f"{display_name} / {id}")
            for id, display_name in Course.objects.values_list("id", "display_name")
        ]
        self.fields["source_course_id"].choices = course_ids

    class Meta:
        model = Course
        fields = (
            "source_course_id",
            "start",
            "end",
            "title_override",
        )


class CourseSerializerField(serializers.Field):
    def to_representation(self, value):
        return str(value.id)


class CourseAccessRoleASerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=64)
    course_id = serializers.ChoiceField([], required=False)
    role = serializers.ChoiceField(
        [
            ("instructor", "instructor"),
            ("staff", "staff"),
            ("beta", "beta tester"),
        ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # course_id
        course_ids = [
            (str(id), f"{display_name} / {id}")
            for id, display_name in Course.objects.values_list("id", "display_name")
        ]
        self.fields["course_id"].choices = course_ids

    class Meta:
        model = CourseAccessRole
        fields = ("username", "course_id", "role")


class CourseAccessRoleSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name="v1:courseaccessrole-detail")
    course = CourseSerializerField(read_only=True)

    class Meta:
        model = CourseAccessRole
        fields = "__all__"
