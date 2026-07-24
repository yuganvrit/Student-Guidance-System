# assessment/serializers/student_skill_result_serializer.py
from rest_framework import serializers
from assessment.models import StudentSkillResult
from skill.serializers.skill_serializer import SkillMiniReadSerializer


class StudentSkillResultSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for student skill results.
    Includes nested skill details for easy frontend consumption.
    """
    skill = SkillMiniReadSerializer(read_only=True)
    assessment_title = serializers.CharField(
        source='student_assessment.assessment.title',
        read_only=True
    )
    assessment_id = serializers.IntegerField(
        source='student_assessment.assessment.id',
        read_only=True
    )

    class Meta:
        model = StudentSkillResult
        fields = [
            'id',
            'assessment_id',
            'assessment_title',
            'skill',
            'score',
            'created_at',
            'updated_at'
        ]
        read_only_fields = fields