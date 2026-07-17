from django.db import models
from base.models import BaseModel
from authentication.models import User
from course.models import CourseBatch

# Create your models here.
class Enrollment(BaseModel):
    STATUS=(
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("partial", "Partial"),
        ("paid", "Paid"),
        ("refunded", "Refunded"),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    batch = models.ForeignKey(CourseBatch, on_delete=models.CASCADE, related_name='enrollments') 
    enrolled_at = models.DateTimeField(auto_now_add=True)
    payment_status= models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "batch"],
                condition=models.Q(is_deleted=False),
                name="unique_active_enrollment"
            )
        ]