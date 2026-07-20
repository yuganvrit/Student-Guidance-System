from rest_framework import serializers
from assessment.models import Assessment
from course.models import Course
from course.serializers.course_serializer import GetMiniCourseSerializer

class AssessmentCreateSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Assessment
        fields = ['title', 'description', 'course', 'passing_score', 'max_attempts', 'assessment_type', 'target_level', 'assessment_phase', 'questions', 'time_minutes', 'is_active']
        
class AssessmentReadSerializer(serializers.ModelSerializer):
    course = GetMiniCourseSerializer(read_only=True)
    class Meta:
        model = Assessment
        fields = ['id', 'title', 'description', 'course', 'passing_score', 'max_attempts', 'assessment_type', 'target_level', 'assessment_phase', 'questions', 'time_minutes', 'is_active', 'created_at', 'updated_at']
        read_only_fields = fields
        
class GetMiniAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['id', 'title', 'course']