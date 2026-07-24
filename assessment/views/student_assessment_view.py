from rest_framework import viewsets
from rest_framework.decorators import action
from skill.models import Skill
from assessment.models import StudentAssessment, AssessmentSkill, StudentSkillResult
from assessment.serializers.student_assessment_serializer import (
    StudentAssessmentReadSerializer,
    StudentAssessmentCreateSerializer,
    StudentAssessmentSubmitSerializer
)
from utils.response_helpers import success_response, error_response
from rest_framework.permissions import AllowAny



class StudentAssessmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing student assessment attempts.
    """
    permission_classes = [AllowAny]
    queryset = StudentAssessment.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'start':
            return StudentAssessmentCreateSerializer
        elif self.action == 'submit':
            return StudentAssessmentSubmitSerializer
        return StudentAssessmentReadSerializer
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'student':
            return self.queryset.filter(student=user)
        return self.queryset
    
    # ------------------------------------------------------------------------
    # START TEST
    # ------------------------------------------------------------------------
    @action(detail=False, url_path='start', methods=['post'])
    def start(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        student_assessment = serializer.save()
        read_serializer = StudentAssessmentReadSerializer(student_assessment)
        
        return success_response(data=read_serializer.data, status_code=201)
    
    # ------------------------------------------------------------------------
    # SUBMIT ANSWERS
    # ------------------------------------------------------------------------
    @action(detail=True, url_path='submit', methods=['post'])
    def submit(self, request, pk=None):
        attempt = self.get_object()
        
        # Validate status
        if attempt.status != StudentAssessment.Status.IN_PROGRESS:
            return error_response(
                errors="Cannot submit. Attempt is not in progress.", 
                status_code=400
            )
        
        # Validate ownership
        if attempt.student != request.user:
            return error_response(
                errors="You can only submit your own attempts.", 
                status_code=403
            )
        
        # Validate submitted data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get data
        answers = serializer.validated_data.get('answers')
        time_taken = serializer.validated_data.get('time_taken_seconds')
        
        # 1. Calculate per-skill scores
        # Returns: {"skill_scores": [{"skill_id": 1, "score": 90}, ...]}
        skill_breakdown = self._calculate_skill_breakdown(attempt.assessment, answers)
        
        # 2. Calculate overall weighted score
        overall_score = self._calculate_overall_score(skill_breakdown, attempt.assessment)
        
        # 3. CREATE StudentSkillResult rows (one per skill)
        for skill_data in skill_breakdown['skill_scores']:
            StudentSkillResult.objects.create(
                student_assessment=attempt,      # links to this test attempt
                skill_id=skill_data['skill_id'],
                score=skill_data['score']
            )
        
        # 4. Complete the parent assessment (only overall score, no skill_breakdown)
        attempt.complete(
            score=overall_score,
            answers=answers,
            time_taken=time_taken
        )
        
        # Return results
        read_serializer = StudentAssessmentReadSerializer(attempt)
        return success_response(data=read_serializer.data, status_code=200)
    
    # ------------------------------------------------------------------------
    # ABANDON TEST
    # ------------------------------------------------------------------------
    @action(detail=True, url_path='abandon', methods=['post'])
    def abandon(self, request, pk=None):
        attempt = self.get_object()
        
        if attempt.status != StudentAssessment.Status.IN_PROGRESS:
            return error_response(
                errors="Can only abandon in-progress attempts.", 
                status_code=400
            )
        
        if attempt.student != request.user:
            return error_response(
                errors="You can only abandon your own attempts.", 
                status_code=403
            )
        
        attempt.abandon()
        
        return success_response(
            data={"message": "Assessment abandoned", "status": attempt.status},
            status_code=200
        )
    
    # ------------------------------------------------------------------------
    # HELPER METHODS
    # ------------------------------------------------------------------------
    def _calculate_skill_breakdown(self, assessment, answers):
        """
        Calculate per-skill scores from answers.
        Returns: {"skill_scores": [{"skill_id": 1, "score": 90}, ...]}
        """
        questions = assessment.questions
        student_answers = answers.get('answers', [])
        
        question_map = {q['id']: q for q in questions}
        skill_stats = {}
        skill_ids = []
        
        for answer in student_answers:
            question_id = answer.get('question_id')
            student_answer = answer.get('answer')
            
            question = question_map.get(question_id)
            if not question:
                continue
            
            skill_id = question.get('skill_id')
            skill_ids.append(skill_id)
            correct_answer = question.get('correct_answer')
            
            if skill_id not in skill_stats:
                skill_stats[skill_id] = {'correct': 0, 'total': 0}
            
            skill_stats[skill_id]['total'] += 1
            
            if student_answer == correct_answer:
                skill_stats[skill_id]['correct'] += 1
        
        skill_scores = []
        for skill_id, stats in skill_stats.items():
            percentage = round((stats['correct'] / stats['total']) * 100) if stats['total'] > 0 else 0
            skill_scores.append({
                'skill_id': skill_id,
                'score': percentage
            })
        
        return {'skill_scores': skill_scores}
        
        
    def _calculate_overall_score(self, skill_breakdown, assessment):
        """Calculate weighted overall score."""
        skill_scores = skill_breakdown.get('skill_scores', [])
        
        total_score = 0
        total_weight = 0
        
        for skill_data in skill_scores:
            skill_id = skill_data.get('skill_id')
            score = skill_data.get('score', 0)
            
            try:
                assessment_skill = AssessmentSkill.objects.get(
                    assessment=assessment,
                    skill_id=skill_id
                )
                weight = assessment_skill.weightage
            except AssessmentSkill.DoesNotExist:
                weight = 100 / len(skill_scores) if skill_scores else 0
            
            total_score += score * weight
            total_weight += weight
        
        return round(total_score / total_weight) if total_weight > 0 else 0