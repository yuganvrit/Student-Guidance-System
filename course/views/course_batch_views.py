from rest_framework import generics
from course.serializers.course_batch_serializer import CourseBatchSerializer
from course.models import CourseBatch

class CourseBatchListCreateView(generics.ListCreateAPIView):
     serializer_class = CourseBatchSerializer
     queryset = CourseBatch.objects.all()

class CourseBatchDetailView(generics.RetrieveUpdateDestroyAPIView):
     serializer_class = CourseBatchSerializer
     queryset = CourseBatch.objects.all()
     