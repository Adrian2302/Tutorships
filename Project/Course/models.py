from django.db import models


# Create your models here.
class Course(models.Model):
    """Model for the User"""
    university = models.CharField(max_length=50)
    course_name = models.CharField(max_length=80)
    description = models.CharField(max_length=250)
    course_clean_name = models.CharField(max_length=80)

class CourseKeyword(models.Model):
    id_course = models.ForeignKey(Course, on_delete=models.CASCADE)
