from django.db import models
from base.models import BaseModel
from authentication.models import User


class StudentCounselor(BaseModel):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='student_counselor',
        limit_choices_to={'role': 'student'}
    )
    counselor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='counselor_students',
        limit_choices_to={'role': 'counselor'}
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'counselor'],
                condition=models.Q(is_active=True),
                name='unique_student_counselor_while_active'
            ),
            models.UniqueConstraint(
                fields=['student'],
                condition=models.Q(is_active=True),
                name='unique_active_counseling_while_active'
            )
        ]
    
    def __str__(self):
        return f"{self.student.username} → {self.counselor.username}"
    
class CounselingSession(BaseModel):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )
    
    student_counselor = models.ForeignKey(
        'StudentCounselor',
        on_delete=models.CASCADE,
        related_name='counseling_sessions'
    )
    scheduled_at = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return (
            f"Session for {self.student_counselor.student.username} "
            f"with {self.student_counselor.counselor.username} "
            f"on {self.scheduled_at.strftime('%Y-%m-%d %H:%M')}"
        )