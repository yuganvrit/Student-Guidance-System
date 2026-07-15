from rest_framework import serializers
from course.models import Course, CourseCategory
from course.serializers.course_category_serializer import GetMiniCourseCategorySerializer

class PostCourseSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CourseCategory.objects.all()
    )
    class Meta:
        model=Course
        fields = "__all__"

class GetMiniCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields=['id', 'title']
        
class GetCourseSerializer(serializers.ModelSerializer):
    categories = GetMiniCourseCategorySerializer(read_only=True, many=True)
    class Meta:
        model=Course
        fields = "__all__"