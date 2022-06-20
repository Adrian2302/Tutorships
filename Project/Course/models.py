from django.db import models


# Create your models here.
class Course(models.Model):
    """Model for the Course"""
    university = models.CharField(max_length=50)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name
