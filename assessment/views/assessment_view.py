from rest_framework import viewsets
from assessment.models import Assessment
from assessment.serializers.assessment_serializer import AssessmentReadSerializer, AssessmentCreateSerializer

class AssessmentViewSet(viewsets.ModelViewSet):
 
    queryset = Assessment.objects.all()
    
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AssessmentReadSerializer
        return AssessmentCreateSerializer