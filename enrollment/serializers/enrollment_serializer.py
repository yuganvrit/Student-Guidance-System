from rest_framework import serializers
from enrollment.models import Enrollment
from course.models import CourseBatch
from authentication.models import User



class EnrollmentCreateSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    batch = serializers.PrimaryKeyRelatedField(queryset=CourseBatch.objects.all())
    
    class Meta:
        model = Enrollment
        fields = ['student', 'batch', 'payment_status']

class EnrollmentDetailSerializer(serializers.ModelSerializer):
    student_details = serializers.SerializerMethodField()
    batch_detail = serializers.SerializerMethodField()
    payment_status_detail = serializers.SerializerMethodField()
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student_details', 'batch_detail',
            'enrolled_at', 'payment_status', 'payment_status_detail',
            'created_at', 'updated_at'
        ]
        
