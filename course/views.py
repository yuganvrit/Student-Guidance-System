# course/views.py
from rest_framework import viewsets, permissions, filters
from .models import Course, CourseBatch
from .serializers import CourseSerializer, CourseBatchSerializer, CourseWithBatchesSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_deleted=False)
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'code']
    ordering_fields = ['title', 'fee', 'duration_weeks']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseWithBatchesSerializer
        return CourseSerializer

class CourseBatchViewSet(viewsets.ModelViewSet):
    queryset = CourseBatch.objects.filter(is_deleted=False)
    serializer_class = CourseBatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['batch_name', 'instructor']

    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset