from django.db import models
from base.models import BaseModel


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
    
    batch_code = models.CharField(max_length=15, unique=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE, related_name='batches' )
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateField(null=True, blank=True)
    end_date=models.DateField(null=True, blank=True)
    max_seats= models.PositiveIntegerField(default=20)
    current_enrollments=models.PositiveIntegerField(default=0)
    schedule = models.JSONField(default=dict)
    
    @property
    def available_seats(self):
        return self.max_seats - self.current_enrollments

    def __str__(self):
        return f"{self.course.title} - Batch {self.batch_number}"