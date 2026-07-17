from django.db import models
from base.models import BaseModel
# Create your models here.
class Skill(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
