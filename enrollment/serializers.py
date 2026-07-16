from rest_framework import serializers
from .models import Enrollment
from course.serializers import CourseBatchSerializer
from authentication.serializers import UserSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class EnrollmentDetailSerializer(EnrollmentSerializer):
    student = UserSerializer(read_only=True)
    batch = CourseBatchSerializer(read_only=True)