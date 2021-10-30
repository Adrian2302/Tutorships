from django.db import models
from Course.models import Course


# Create your models here.
class Tutorship(models.Model):
    """Model for the Tutorship"""
    max_people = models.IntegerField()
    state = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=250)


class TutorshipCourse(models.Model):
    """Model for the CourseTutorship"""
    tutorship = models.ForeignKey(Tutorship, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=0)
