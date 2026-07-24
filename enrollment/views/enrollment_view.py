from rest_framework import viewsets
from enrollment.models import Enrollment
from enrollment.serializers.enrollment_serializer import  EnrollmentCreateSerializer, EnrollmentDetailSerializer
from rest_framework.permissions import IsAdminUser

class EnrollmentView(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related('student', 'batch', 'batch__mentor')
    permission_classes=[IsAdminUser]
    ordering=['-created_at']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EnrollmentCreateSerializer
        return EnrollmentDetailSerializer