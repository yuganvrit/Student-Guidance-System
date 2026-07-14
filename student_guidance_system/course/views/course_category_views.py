from rest_framework import generics

from course.models import CourseCategory
from course.serializers.course_category_serializer import CourseCategorySerializer


class CourseCategoryListCreateView(generics.ListCreateAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer

    


class CourseCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    