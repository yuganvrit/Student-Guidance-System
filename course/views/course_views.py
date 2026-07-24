from rest_framework import viewsets
from course.models import Course
from course.serializers.course_serializer import PostCourseSerializer, GetCourseSerializer
from course.permissions import AdminOnlyPost
from rest_framework.generics import GenericAPIView
class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [AdminOnlyPost]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetCourseSerializer
        return PostCourseSerializer
    
