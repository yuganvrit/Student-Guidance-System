from rest_framework import serializers
from career.models import Career
from skill.models import Skill
from skill.serializers.skill_serializer import SkillMiniReadSerializer


class CareerCreateSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True, required=False)
    class Meta:
        model = Career
        fields = ['title', 'description', 'average_salary', 'skills', 'industry']
        
class CareerReadSerializer(serializers.ModelSerializer):
    skills = SkillMiniReadSerializer(many=True, read_only=True)
    class Meta:
        model = Career
        fields = ['id', 'title', 'description', 'average_salary', 'skills', 'industry']