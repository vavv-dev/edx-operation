from rest_framework import serializers

from edx_operation.apps.notification.models import StudentNotification


class StudentNotificationSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name="v1:studentnotification-detail")

    class Meta:
        model = StudentNotification
        fields = "__all__"

    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True
        return fields
