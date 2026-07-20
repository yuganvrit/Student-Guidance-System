from rest_framework import viewsets
from assessment.models import AssessmentSkill
from assessment.serializers.assessment_skill_serializer import AssessmentSkillReadSerializer, AssessmentSkillCreateSerializer

class AssessmentSkillViewSet(viewsets.ModelViewSet):
 
    queryset = AssessmentSkill.objects.all()
    
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AssessmentSkillReadSerializer
        return AssessmentSkillCreateSerializer