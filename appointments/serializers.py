# appointments/serializers.py
from rest_framework import serializers
from .models import Appointment
from authentication.serializers import UserSerializer
from course.serializers import CourseSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        # Ensure the student has role='student'
        if data['student'].role != 'student':
            raise serializers.ValidationError({"student": "Selected user is not a student."})
        # Ensure the advisor has role='advisor'
        if data['advisor'].role != 'advisor':
            raise serializers.ValidationError({"advisor": "Selected user is not an advisor."})
        return data

class AppointmentDetailSerializer(AppointmentSerializer):
    student = UserSerializer(read_only=True)
    advisor = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)