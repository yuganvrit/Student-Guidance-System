from rest_framework import serializers
from assessment.models import Assessment
from skill.models import Skill
from skill.serializers.skill_serializer import SkillMiniReadSerializer
from assessment.serializers.assessment_serializer import GetMiniAssessmentSerializer

class AssessmentSkillCreateSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(queryset=Assessment.objects.all(),allow_null=True)
    skill = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(),allow_null=True)
    class Meta:
        model = Assessment
        fields = ['assessment', 'skill', 'weightage', 'is_active', 'question_count']
        

class AssessmentSkillReadSerializer(serializers.ModelSerializer):
    assessment = GetMiniAssessmentSerializer(read_only=True)
    skill = SkillMiniReadSerializer(read_only=True)
    class Meta:
        model = Assessment
        fields = ['assessment', 'skill', 'weightage', 'question_count']
        
