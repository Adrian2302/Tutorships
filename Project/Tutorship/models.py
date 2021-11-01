from django.db import models
from Course.models import Course
from Student.models import Request


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
