from rest_framework import serializers
from assessment.models import Assessment, StudentAssessment
from authentication.models import User
from authentication.serializers.student_register_serializer import StudentUserMiniSerializer
from assessment.serializers.assessment_serializer import GetMiniAssessmentSerializer

# ─────────────────────────────────────────────
# START TEST (Student clicks "Start")
# ─────────────────────────────────────────────

class StudentAssessmentCreateSerializer(serializers.ModelSerializer):
    """
    Student picks which assessment to take.
    System creates attempt with auto-increment number.
    """
    assessment = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all()
    )
    
    class Meta:
        model = StudentAssessment
        fields = ['assessment'] 
    
    def validate(self, data):
        request = self.context.get('request')
        student = request.user if request else None
        
        if not student:
            raise serializers.ValidationError("Authentication required.")
        
        assessment = data['assessment']
        
        # Check max attempts
        completed = StudentAssessment.objects.filter(
            student=student,
            assessment=assessment,
            status=StudentAssessment.Status.COMPLETED
        ).count()
        
        if completed >= assessment.max_attempts:
            raise serializers.ValidationError(
                f"Maximum attempts ({assessment.max_attempts}) reached."
            )
        
        # Check in-progress
        in_progress = StudentAssessment.objects.filter(
            student=student,
            assessment=assessment,
            status=StudentAssessment.Status.IN_PROGRESS
        ).exists()
        
        if in_progress:
            raise serializers.ValidationError(
                "Complete or abandon your current attempt first."
            )
        
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        student = request.user
        
        # Auto-increment attempt_number
        last = StudentAssessment.objects.filter(
            student=student,
            assessment=validated_data['assessment']
        ).order_by('-attempt_number').first()
        
        attempt_number = (last.attempt_number + 1) if last else 1
        
        return StudentAssessment.objects.create(
            student=student,
            assessment=validated_data['assessment'],
            attempt_number=attempt_number,
            status=StudentAssessment.Status.IN_PROGRESS
        )

# ─────────────────────────────────────────────
# SUBMIT ANSWERS (Student clicks "Submit")
# ─────────────────────────────────────────────

class StudentAssessmentSubmitSerializer(serializers.Serializer):
    """
    Student submits answers.
    System calculates score and skill_breakdown.
    """
    answers = serializers.JSONField(required=True)
    time_taken_seconds = serializers.IntegerField(required=False, allow_null=True)
    
    def validate_answers(self, value):
        if not isinstance(value, dict) or 'answers' not in value:
            raise serializers.ValidationError(
                "Format: {'answers': [{'question_id': 1, 'answer': 'A'}, ...]}"
            )
        return value

# ─────────────────────────────────────────────
# READ RESULTS
# ─────────────────────────────────────────────

class StudentAssessmentReadSerializer(serializers.ModelSerializer):
    """
    Read-only. Shows all results including computed properties.
    """
    student = StudentUserMiniSerializer(read_only=True)
    assessment = GetMiniAssessmentSerializer(read_only=True)
    
    class Meta:
        model = StudentAssessment
        fields = [
            'id', 'student', 'assessment',
            'answers', 'skill_breakdown', 'score', 
            'has_passed', 'weak_skills',  
            'attempt_number', 'status', 
            'time_taken_seconds', 'completed_at',
            'created_at', 'updated_at'
        ]
        
# class GetMiniStudentAssessmentReadSerializer(serializers.ModelSerializer):
#     """
#     Read-only. shows only the essential details of a student assessment.
#     """
#     student = StudentProfileReadSerializer(read_only=True)
#     assessment = GetMiniAssessmentSerializer(read_only=True)
    
#     class Meta:
#         model = StudentAssessment
#         fields = [
#             'id', 'student', 'assessment',
#             'answers', 'skill_breakdown', 'score', 
#             'has_passed', 'weak_skills',  
#             'attempt_number', 'status', 
#             'time_taken_seconds', 'completed_at',
#             'created_at', 'updated_at'
#         ]
        
