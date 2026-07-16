from rest_framework import viewsets
from course.models import Course
from course.serializers.course_serializer import PostCourseSerializer, GetCourseSerializer

class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetCourseSerializer
        return PostCourseSerializer
    
