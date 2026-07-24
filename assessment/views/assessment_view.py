from rest_framework import viewsets
from assessment.models import Assessment
from assessment.serializers.assessment_serializer import AssessmentReadSerializer, AssessmentCreateSerializer
from rest_framework.permissions import AllowAny

class AssessmentViewSet(viewsets.ModelViewSet):
 
    queryset = Assessment.objects.all()
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AssessmentReadSerializer
        return AssessmentCreateSerializer