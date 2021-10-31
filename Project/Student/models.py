from django.db import models
from UserAuthentication.models import User
from Session.models import Session
from Modality.models import Modality
from Course.models import Course

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

    user_requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_requester')
    tutor_requested = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_requested')
    session_requested = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_requested')
    modality_requested = models.ForeignKey(Modality, on_delete=models.CASCADE, related_name='modality_requested')
    course_requested = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_requested')
    num_requesters = models.IntegerField(default=0)
    state = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING)
    meeting_type = models.CharField(max_length=2, choices=MEETING_CHOICES, default=ZOOM)
    tutor_comment = models.TextField(null=True)
    student_comment = models.TextField(null=True)
    date_start = models.DateTimeField()                             # Fecha de inicio solicitada para la tutoría.
    date_end = models.DateTimeField()                               # Fecha de fin solicitada para la tutoría.
    date_request = models.DateTimeField(auto_now_add=True)          # Fecha de solicitud de tutoría.
    date_resolution = models.DateTimeField(null=True)               # Fecha de resolución de tutoría.



class Requesters(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    user_requester = models.ForeignKey(User, on_delete=models.CASCADE)

