from django.db import connections
from django.db import models
from django.db.models.fields.related import ForeignKey
from datetime import datetime, date

# Create your models here.
class Tutorship(models.Model):
    """Model for the Tutorship"""
    max_people = models.IntegerField()
    amount_per_person = models.IntegerField()
    increment_per_half_hour = models.IntegerField()
    state = models.IntegerField()
    type_session = models.IntegerField()
    type_mode = models.IntegerField()

class CourseTutorship(models.Model):
    """Model for the CourseTutorship"""
    id_tutorship = models.ForeignKey(Tutorship, on_delete=models.CASCADE)

class TutorshipAvailableSchedule(models.Model):
    """Model for the Tutorship"""
    id_tutorship = models.ForeignKey(Tutorship, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False, auto_now=False, blank=True)
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    