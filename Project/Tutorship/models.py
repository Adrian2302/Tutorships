from django.db import connections
from django.db import models
from django.db.models.fields.related import ForeignKey
from datetime import datetime, date
from Course.models import Course
from UserAuthentication.models import User


# Create your models here.
class Tutorship(models.Model):
    """Model for the Tutorship"""
    max_people = models.IntegerField()
    state = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=250)
    # amount_per_person = models.IntegerField()
    # increment_per_half_hour = models.IntegerField()
    # type_session = models.IntegerField()
    # type_mode = models.IntegerField()


class TutorshipCourse(models.Model):
    """Model for the CourseTutorship"""
    tutorship = models.ForeignKey(Tutorship, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=0)


class TutorshipAvailableSchedule(models.Model):
    """Models for tha tables describing the hours the tutor has available."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
