from django.db import connections
from django.db import models
from django.db.models.fields.related import ForeignKey
from datetime import datetime, date
from Course.models import Course
from Session.models import Session
from Modality.models import Modality
from Payment.models import Payment
from UserAuthentication.models import User


# Create your models here.
class Tutor(models.Model):
    """Model for the Tutor"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_per_person = models.IntegerField(default=0)
    increment_per_half_hour = models.IntegerField(default=0)
    payment_type = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    session_type = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    modality_type = models.ForeignKey(Modality, on_delete=models.CASCADE, null=True)


class TutorAvailableSchedule(models.Model):
    """Models for tha tables describing the hours the tutor has available."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
