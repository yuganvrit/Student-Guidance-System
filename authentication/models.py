from django.db import models
from django.contrib.auth.models import AbstractUser
from base.models import BaseModel


#custom user model 
class User(AbstractUser,BaseModel):
    ROLE_CHOICES = (
        ('super_admin','Super Admin'),
        ('student', 'Student'),      
        ('mentor', 'Mentor'),
        ('counselor','Counselor')                      
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    last_login = models.DateTimeField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username'],
                condition=models.Q(is_deleted=False),
                name='unique_user_username_when_not_deleted'
            ),
            models.UniqueConstraint(
                fields=['phone'],
                condition=models.Q(is_deleted=False) & ~models.Q(phone=''),
                name='unique_user_phone_when_not_deleted'
            ),
        ]

    def __str__(self):
        return self.email


class CustomFormatDateField(models.DateField):
    def formfield(self, **kwargs):
        # Automatically injects custom format settings whenever a form relies on this model field
        defaults = {
            'input_formats': ['%d/%m/%Y', '%d-%m-%Y'],
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class BaseProfile(BaseModel):
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='profiles/')
    address = models.CharField(max_length=100)
    birth_date = CustomFormatDateField(null=True, blank=True)

    class Meta:
        abstract = True
    
class StudentProfile(BaseProfile):
    EDUCATION_LEVEL_CHOICES = (
        ('high_school', 'High School'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('other', 'Other'),
    )
    PREFERRED_LEARNING_MODE_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('hybrid', 'Hybrid'),
    )
    
    student = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        limit_choices_to={'role': 'student'}
    )
    education_level = models.CharField(
        max_length=20,
        choices=EDUCATION_LEVEL_CHOICES,
        blank=True,
        null=True
    )
    preferred_learning_mode = models.CharField(
        max_length=20,
        choices=PREFERRED_LEARNING_MODE_CHOICES,
        blank=True,
        null=True
    )
    career = models.ForeignKey('career.Career', on_delete=models.SET_NULL, blank=True, null=True, related_name='student_profiles')

    def __str__(self):
        return f"Profile of {self.student.username}"
    
class CounselorProfile(BaseProfile):
    counselor = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='counselor_profile',
        limit_choices_to={'role': 'counselor'}
    )
    specialization = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    
    
    def __str__(self):
        return f"Profile of {self.counselor.username}"
    
class MentorProfile(BaseProfile):
    mentor = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='mentor_profile',
        limit_choices_to={'role': 'mentor'}
    )
    expertise_area = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    skills = models.ManyToManyField('skill.Skill', related_name='mentors_skill')
    
    def __str__(self):
        return f"Profile of {self.mentor.username}"