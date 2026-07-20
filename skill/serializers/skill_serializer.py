from rest_framework.serializers import ModelSerializer
from skill.models import Skill


class SkillDetailSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        
class SkillCreateSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description']
        
class SkillMiniReadSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']