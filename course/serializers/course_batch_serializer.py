from rest_framework import serializers
from course.models import Course, CourseBatch
from course.serializers.course_serializer import GetMiniCourseSerializer

class CourseBatchSerializer(serializers.ModelSerializer):
    course_details = serializers.SerializerMethodField()
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True)
    class Meta:
        model = CourseBatch
        fields = "__all__"
        
    def get_course_details(self, obj):
        return GetMiniCourseSerializer(obj.course).data