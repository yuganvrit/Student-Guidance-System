from django.db import models
from base.models import BaseModel
from authentication.models import User
from course.models import CourseBatch
from assessment.models import AssessmentResult

class Enrollment(BaseModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    batch = models.ForeignKey(CourseBatch, on_delete=models.CASCADE, related_name='enrollments')
    assessment_result = models.ForeignKey(AssessmentResult, on_delete=models.SET_NULL, null=True, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'batch')  # prevent duplicate enrollment

    def __str__(self):
        return f"{self.student.email} -> {self.batch}"