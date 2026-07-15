from rest_framework import serializers
from course.models import Course

class CourseSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )
    class Meta:
        model=Course
        fields = "__all__"
