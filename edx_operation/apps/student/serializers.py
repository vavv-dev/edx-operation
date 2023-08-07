from datetime import datetime

from rest_framework import serializers

from edx_operation.apps.student.models import Student

THIS_YEAR = datetime.now().year


class StudentSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name="v1:student-detail")

    class Meta:
        model = Student
        fields = "__all__"


class StudentCSerializer(serializers.ModelSerializer):
    YEAR_OF_BIRTH_CHOICES = [(str(year), str(year)) for year in range(THIS_YEAR - 100, THIS_YEAR)]

    year_of_birth = serializers.ChoiceField(choices=YEAR_OF_BIRTH_CHOICES)
    initial_password = serializers.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # year_of_birth
        self.fields["year_of_birth"].initial = THIS_YEAR - 35

    class Meta:
        model = Student
        fields = (
            "name",
            "username",
            "email",
            "year_of_birth",
            "initial_password",
        )
