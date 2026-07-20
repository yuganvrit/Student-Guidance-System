from django.db import models
from base.models import BaseModel
from course.models import Course
from django.core.validators import MinValueValidator, MaxValueValidator

class Assessment(BaseModel):
    
    class AssessmentType(models.TextChoices):
        CAREER_APTITUDE = 'career_aptitude', 'Career Aptitude'
        COURSE_PLACEMENT = 'course_placement', 'Course Placement'
        COURSE_QUIZ = 'course_quiz', 'Course Quiz'
        COURSE_FINAL = 'course_final', 'Course Final'
        SKILL_ASSESSMENT = 'skill_assessment', 'Skill Assessment'
        
    class TargetLevel(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'
        
    class AssessmentPhase(models.TextChoices):
        PLACEMENT='placement', 'Placement'
        PROGRESS='progress', 'Progress'
        FINAL = 'final', 'Final'
        CERTIFICATION = 'certification', 'Certification'
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assessments', null=True, blank=True)
    passing_score = models.PositiveBigIntegerField(default=60, validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_attempts = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    assessment_type = models.CharField(max_length=20, choices=AssessmentType.choices, default=AssessmentType.COURSE_QUIZ)
    target_level = models.CharField(max_length=20, choices=TargetLevel.choices, default=TargetLevel.BEGINNER)
    assessment_phase = models.CharField(max_length=20, choices=AssessmentPhase.choices, default=AssessmentPhase.PLACEMENT)
    questions = models.JSONField(default=list, blank=True)  # Store questions as a list of dictionaries
    time_minutes = models.PositiveIntegerField(default=60)  # Duration of the assessment in minutes
    is_active= models.BooleanField(default=True)

    class Meta:
        indexes = [
        models.Index(fields=['assessment_type'], name='idx_assessment_type'),
        models.Index(fields=['course'], name='idx_assessment_course'),
        models.Index(fields=['target_level'], name='idx_assessment_level'),
        models.Index(fields=['assessment_phase'], name='idx_assessment_phase'),
        models.Index(fields=['is_active'], name='idx_assessment_active'),
    ]
        ordering=['-created_at']
        constraints=[
            models.UniqueConstraint(fields=['title'], condition= models.Q(is_deleted=False), name='unique_active_assessment_title'),
            models.CheckConstraint( condition=models.Q(passing_score__gte=0) & models.Q(passing_score__lte=100), name='valid_passing_score'),
            models.CheckConstraint(condition=models.Q(max_attempts__gte=1), name='valid_max_attempts')
        ]

    def __str__(self):
        return self.title
    

class AssessmentSkill(BaseModel):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='assessment_skills')
    skill = models.ForeignKey('skill.Skill', on_delete=models.CASCADE, related_name='skill_assessments')
    weightage=models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    question_count=models.PositiveIntegerField(default=1)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['assessment', 'skill'], condition= models.Q(is_deleted=False), name='unique_active_assessment_skill'),
        ]
        ordering=['-created_at']

    def __str__(self):
        return f"{self.assessment.title} - {self.skill.name}"
    
class StudentAssessment(BaseModel):
    
    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        ABANDONED = 'abandoned', 'Abandoned'
    
    student = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='student_assessments')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='student_assessments')
    answers = models.JSONField(default=dict, blank=True)  # Store answers as a list of dictionaries
    skill_breakdown=models.JSONField(default=dict, blank=True)
    score = models.PositiveIntegerField(null=True,blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    attempt_number = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    time_taken_seconds = models.PositiveIntegerField(null=True, blank=True)  # Time taken to complete the assessment in seconds
    completed_at = models.DateTimeField(null=True, blank=True)
    
    
#the answers JSON structure is expected to be like this:
#{"answers": [{"question_id": 1, "answer": "B", "is_correct": true}, ...]}

#the skill_breakdown JSON structure is expected to be like this:
#   {
#     "skill_scores": [
#       {"skill_id": 1, "score": 90},
#       {"skill_id": 2, "score": 70},
#       {"skill_id": 3, "score": 40},
#       {"skill_id": 4, "score": 10}
#     ]
#   }
    class Meta:
        
        constraints = [
        # Prevent duplicate in-progress attempts for same student+assessment
        models.UniqueConstraint(
            fields=['student', 'assessment'],
            condition=models.Q(status='in_progress'),
            name='unique_in_progress_assessment'
        ),
        models.UniqueConstraint(
            fields=['student', 'assessment','attempt_number'],
            condition=models.Q(status='is_completed'),
            name='unique_student_assessment_attempt'
        ),
    ]
        ordering=['-created_at']

    def __str__(self):
        return f"{self.student.username} - {self.assessment.title} (Attempt {self.attempt_number})"
    
    @property
    def has_passed(self):
        if self.score is None:
            return False
        return self.score >= self.assessment.passing_score
    
    @property
    def weak_skills(self):
        threshold=50
        weak_skills = []
        for skill_data in self.skill_breakdown.get('skill_scores', []):
            if skill_data.get('score', 0) < threshold:
                weak_skills.append(skill_data)
        return weak_skills
    

    def complete(self, score, skill_breakdown, answers=None, time_taken=None):
        """Mark as completed with results. Called when student submits."""
        from django.utils import timezone
        
        self.score = score
        self.skill_breakdown = skill_breakdown
        if answers:
            self.answers = answers
        if time_taken:
            self.time_taken_seconds = time_taken
        
        self.status = self.Status.COMPLETED
        self.completed_at = timezone.now()
        self.save()
    
    def abandon(self):
        """Mark as abandoned. Called when student leaves without finishing."""
        self.status = self.Status.ABANDONED
        self.save()