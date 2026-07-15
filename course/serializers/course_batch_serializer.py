from rest_framework import serializers
from course.models import CourseBatch
from .course_serializer import GetMiniCourseSerializer

class CourseBatchSerializer(serializers.ModelSerializer):
    batch_code = serializers.CharField(read_only=True)
    class Meta:
        model = CourseBatch
        fields = "__all__"

    
class GetCourseBatchSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    class Meta:
        model = CourseBatch
        fields = "__all__"

    
    def get_course(self,obj):
        return GetMiniCourseSerializer(obj.course).data