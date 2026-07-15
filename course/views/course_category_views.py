from rest_framework import viewsets

from course.models import CourseCategory
from course.serializers.course_category_serializer import CourseCategorySerializer


class CourseCategoryView(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
