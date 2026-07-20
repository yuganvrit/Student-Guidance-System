from rest_framework import serializers
from assessment.models import AssessmentSkill, Assessment
from skill.models import Skill
from skill.serializers.skill_serializer import SkillMiniReadSerializer
from assessment.serializers.assessment_serializer import GetMiniAssessmentSerializer

class AssessmentSkillCreateSerializer(serializers.ModelSerializer):
    assessment = serializers.PrimaryKeyRelatedField(queryset=Assessment.objects.all())
    skill = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all())
    class Meta:
        model = AssessmentSkill
        fields = ['assessment', 'skill', 'weightage', 'question_count']
        

class AssessmentSkillReadSerializer(serializers.ModelSerializer):
    assessment = GetMiniAssessmentSerializer(read_only=True)
    skill = SkillMiniReadSerializer(read_only=True)
    class Meta:
        model = AssessmentSkill
        fields = ['assessment', 'skill', 'weightage', 'question_count']
        
