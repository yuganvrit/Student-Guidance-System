from rest_framework import viewsets
from course.serializers.course_batch_serializer import CourseBatchSerializer
from course.models import CourseBatch

class CourseBatchView(viewsets.ModelViewSet):
     serializer_class = CourseBatchSerializer
     queryset = CourseBatch.objects.all()
