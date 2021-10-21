from django.db import connections
from django.db import models
from django.db.models.fields.related import ForeignKey
from datetime import datetime, date

# Create your models here.
class Tutorship(models.Model):
    """Model for the Tutorship"""
    maxPeople = models.IntegerField()
    amountPerPerson = models.IntegerField()
    incrementPerHalfHour = models.IntegerField()
    state = models.IntegerField()
    typeSession = models.IntegerField()
    typeMode = models.IntegerField()

class CourseTutorship(models.Model):
    """Model for the CourseTutorship"""
    idTutorship = models.ForeignKey(Tutorship, on_delete=models.CASCADE)

class TutorshipAvailableSchedule(models.Model):
    """Model for the Tutorship"""
    idTutorship = models.ForeignKey(Tutorship, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False, auto_now=False, blank=True)
    startHour = models.TimeField()
    endHour = models.TimeField()
    