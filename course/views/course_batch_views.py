from rest_framework import generics
from course.serializers.course_batch_serializer import (
    CourseBatchSerializer,
    GetCourseBatchSerializer
)
from course.models import CourseBatch

class CourseBatchListCreateView(generics.ListCreateAPIView):
     def get_serializer_class(self):
          if self.request.method == 'GET':
               return GetCourseBatchSerializer
          return CourseBatchSerializer
     queryset = CourseBatch.objects.all()

class CourseBatchDetailView(generics.RetrieveUpdateDestroyAPIView):
     def get_serializer_class(self):
          if self.request.method == 'GET':
               return GetCourseBatchSerializer
          return CourseBatchSerializer
     queryset = CourseBatch.objects.all()
     