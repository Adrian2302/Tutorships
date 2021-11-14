from django.db import models
from Course.models import Course
from Student.models import Request
from UserAuthentication.models import User
from django.utils import timezone


# Create your models here.
class Tutorship(models.Model):
    """Model for the Tutorship"""

    APPROVED = 'AP'
    DONE = 'DN'
    STATUS_CHOICES = (
        (APPROVED, 'Aprobada'),
        (DONE, 'Realizada'),
    )

    max_people = models.IntegerField()
    state = models.CharField(max_length=2, choices=STATUS_CHOICES, default=APPROVED)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=250)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, blank=True, null=True)

    def set_done(self):
        self.state = self.DONE
        self.save()


class TutorshipScore(models.Model):
    """Model for the TutorshipScore"""
    tutorship = models.ForeignKey(Tutorship, on_delete=models.CASCADE)
    score = models.IntegerField()
    student_comment = models.TextField(null=True)


class RequestNotification(models.Model):
    """Model for the notifications."""
    NEW_REQUEST = 'RE'
    ACCEPTED_REQUEST = 'AR'
    REJECTED_REQUEST = 'RR'
    TYPES = (
        (NEW_REQUEST, 'Nueva solicitud'),
        (ACCEPTED_REQUEST, 'Solicitud aceptada'),
        (REJECTED_REQUEST, 'Solicitud rechazada'),
    )
    notification_type = models.CharField(max_length=2, choices=TYPES)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user', null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user', null=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default=False) 

