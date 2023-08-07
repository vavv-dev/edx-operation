from rest_framework import serializers

from edx_operation.apps.forum.models import Post


class CourseSerializerField(serializers.Field):
    def to_representation(self, value):
        return str(value.id)


class PostSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name="v1:post-detail")
    course = CourseSerializerField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
