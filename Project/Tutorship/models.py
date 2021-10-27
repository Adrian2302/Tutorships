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
    amount_per_person = models.IntegerField()
    increment_per_half_hour = models.IntegerField()
    type_session = models.IntegerField()
    type_mode = models.IntegerField()


class CourseTutorship(models.Model):
    """Model for the CourseTutorship"""
    id_tutorship = models.ForeignKey(Tutorship, on_delete=models.CASCADE)
    id_course = models.ForeignKey(Course, on_delete=models.CASCADE, default=0)


class TutorshipAvailableSchedule(models.Model):
    """Model for the Tutorship"""
    id_tutorship = models.ForeignKey(Tutorship, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False, auto_now=False, blank=True)
    start_hour = models.TimeField()
    end_hour = models.TimeField()


class TutorAvailableSchedule(models.Model):
    """Models for tha tables describing the hours the tutor has available."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
