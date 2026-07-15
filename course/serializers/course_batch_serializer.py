from rest_framework import serializers
from course.models import CourseBatch

class CourseBatchSerializer(serializers.ModelSerializer):
    course = serializers.CharField(source='course.title', read_only=True)
    class Meta:
        model = CourseBatch
        fields = "__all__"