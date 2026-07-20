from rest_framework import viewsets
from assessment.models import AssessmentSkill
from assessment.serializers.assessment_skill_serializer import AssessmentSkillReadSerializer, AssessmentSkillCreateSerializer
from rest_framework.permissions import AllowAny

class AssessmentSkillViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = AssessmentSkill.objects.all()
    
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AssessmentSkillReadSerializer
        return AssessmentSkillCreateSerializer