from rest_framework import serializers
from course.models import CourseBatch
from course.serializers.course_serializer import GetMiniCourseSerializer

class CourseBatchSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    class Meta:
        model = CourseBatch
        fields = "__all__"
        
    def get_course(self, obj):
        return GetMiniCourseSerializer(obj.course).data