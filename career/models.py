from base.models import BaseModel
from django.db import models
from skill.models import Skill

class Career(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    average_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    skills = models.ManyToManyField(Skill, through='CareerSkill')
    industry = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class CareerSkill(BaseModel):
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='career_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='skill_careers')
    required_level= models.PositiveIntegerField(default=1)
    weightage = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['career', 'skill'], name='unique_career_skill')
        ]
    
    def __str__(self):
        return f"{self.career.title} - {self.skill.name}"
    
class CareerPath(BaseModel):
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='career_paths')
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='career_paths')
    sequence_number = models.PositiveIntegerField(default=1)
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['career', 'sequence_number'], name='unique_sequence_number_per_career'),
            models.UniqueConstraint(fields=['career', 'course'], name='unique_course_per_career')
        ]
    
    def __str__(self):
        return f"Path {self.sequence_number} - {self.career.title}"
    
