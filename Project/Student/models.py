from django.db import models
from UserAuthentication.models import User
from Tutorship.models import Tutorship


# Create your models here.
class Request(models.Model):

    PENDING = 'PN'
    APPROVED = 'AP'
    DENIED = 'DD'
    DONE = 'DN'
    STATUS_CHOICES = (
        (PENDING, 'Pendiente'),
        (APPROVED, 'Aprobada'),
        (DENIED, 'Rechazada'),
        (DONE, 'Realizada'),
    )

    ZOOM = 'ZO'
    DISCORD = 'DI'
    MEETUP = 'ME'
    MICROSOFT_TEAMS = 'MT'
    PLACE = 'PL'
    MEETING_CHOICES = (
        (ZOOM, 'Zoom'),
        (DISCORD, 'Discord'),
        (MEETUP, 'Meetup'),
        (MICROSOFT_TEAMS, 'Microsoft Teams'),
        (PLACE, 'Lugar físico'),
    )

    tutorship = models.ForeignKey(Tutorship, on_delete=models.CASCADE)
    user_requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_requester')
    num_requesters = models.IntegerField(default=0)
    state = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING)
    meeting_type = models.CharField(max_length=2, choices=MEETING_CHOICES, default=ZOOM)
    tutor_comment = models.TextField()
    student_comment = models.TextField()
    date_start = models.DateTimeField(auto_now_add=True)            # Fecha de inicio solicitada para la tutoría.
    date_end = models.DateTimeField()                               # Fecha de fin solicitada para la tutoría.
    date_request = models.DateTimeField(auto_now_add=True)          # Fecha de solicitud de tutoría.
    date_resolution = models.DateTimeField()                        # Fecha de resolución de tutoría.


class Requesters(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    user_requester = models.ForeignKey(User, on_delete=models.CASCADE)

