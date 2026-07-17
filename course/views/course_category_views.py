from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from course.models import CourseCategory
from course.serializers.course_category_serializer import CourseCategorySerializer
from course.permissions import AdminOnlyPost


class CourseCategoryView(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    permission_classes=[AdminOnlyPost]
    serializer_class = CourseCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at']
    ordering = ['-created_at']
    

# class CourseCategoryListCreateView(generics.ListCreateAPIView):
#     queryset = CourseCategory.objects.all()
#     serializer_class = CourseCategorySerializer

    


# class CourseCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CourseCategory.objects.all()
#     serializer_class = CourseCategorySerializer
    
