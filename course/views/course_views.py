from rest_framework import generics
from course.models import Course
from course.serializers.course_serializer import CourseSerializer,GetCourseSerializer

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetCourseSerializer
        return CourseSerializer

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetCourseSerializer
        return CourseSerializer

