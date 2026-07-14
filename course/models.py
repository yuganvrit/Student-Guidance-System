from django.db import models
from base.models import BaseModel


class CourseCategory(BaseModel):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.title