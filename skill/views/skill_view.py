from rest_framework import viewsets
from skill.models import Skill
from skill.serializers.skill_serializer import SkillDetailSerializer, SkillCreateSerializer

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return SkillCreateSerializer
        return SkillDetailSerializer