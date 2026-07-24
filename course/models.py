from django.db import models
from base.models import BaseModel
from authentication.models import User


class CourseCategory(BaseModel):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.title
    
class Course(BaseModel):
    LEVEL_CHOICES=(
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    )
    
    title = models.CharField(max_length=50)
    prefix = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=200)
    categories = models.ManyToManyField(CourseCategory, related_name="courses")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    price= models.DecimalField(max_digits=10, decimal_places=2)
    is_active=models.BooleanField(default=True)
    duration= models.DurationField(
        help_text="e.g., 3 hours, 2 weeks",
        null=True,
        blank=True
        )
    
    def __str__(self):
        return self.title
    
class CourseBatch(BaseModel):
    
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    )
    
    batch_code = models.CharField(max_length=15, null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE, related_name='batches' )
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    start_date = models.DateField(null=True, blank=True)
    end_date=models.DateField(null=True, blank=True)
    max_seats= models.PositiveIntegerField(default=20)
    current_enrollments=models.PositiveIntegerField(default=0)
    schedule = models.JSONField(default=dict)
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'mentor'}, related_name='mentored_batches')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['batch_code'],
                condition = models.Q(is_deleted=False),
                name='unique_batch_code_not_deleted'
            )
        ]
    
    def save(self, *args, **kwargs):
        if not self.batch_code:
            count = CourseBatch.objects.filter(course=self.course).count()
            prefix = self.course.prefix
            self.batch_code = f'{prefix}-{count+1}'
        return super().save(*args, **kwargs)
        
    
    @property
    def available_seats(self):
        return self.max_seats - self.current_enrollments

    def __str__(self):
        return self.batch_code
