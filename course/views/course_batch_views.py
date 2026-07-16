from rest_framework import viewsets
from course.serializers.course_batch_serializer import CourseBatchSerializer
from course.models import CourseBatch
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,DjangoObjectPermissions
from course.permissions import IsMentor

class CourseBatchView(viewsets.ModelViewSet):
     permission_classes = [IsMentor]
     serializer_class = CourseBatchSerializer
     queryset = CourseBatch.objects.all()

     