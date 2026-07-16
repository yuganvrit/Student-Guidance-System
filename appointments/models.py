# appointments/models.py
from django.db import models
from base.models import BaseModel
from authentication.models import User
from course.models import Course

class Appointment(BaseModel):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments_as_student',
        limit_choices_to={'role': 'student'}   # only allow users with role='student'
    )
    advisor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments_as_advisor',
        limit_choices_to={'role': 'advisor'}   # only allow users with role='advisor'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    scheduled_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.email} ↔ {self.advisor.email} @ {self.scheduled_time}"

    class Meta:
        ordering = ['scheduled_time']