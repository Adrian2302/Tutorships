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

    user_requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_requester')
    tutor_requested = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_requested')
    num_requesters = models.IntegerField(default=0)
    state = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING)
    meeting_type = models.CharField(max_length=2, choices=MEETING_CHOICES, default=ZOOM)
    tutor_comment = models.TextField()
    student_comment = models.TextField()
    date_start = models.DateTimeField(auto_now_add=True)            # Fecha de inicio solicitada para la tutoría.
    date_end = models.DateTimeField()                               # Fecha de fin solicitada para la tutoría.
    date_request = models.DateTimeField(auto_now_add=True)          # Fecha de solicitud de tutoría.
    date_resolution = models.DateTimeField()                        # Fecha de resolución de tutoría.

    def display_fullname_requester(self):
        return self.user_requester.get_full_name()

    def display_meeting_type(self):
        for choice in self.MEETING_CHOICES:
            if choice[0] == self.meeting_type:
                return choice[1]

    @property
    def is_expired(self):
        if datetime.now() > self.date_start:
            return True
        return False

    @property
    def is_approved(self):
        return self.state == self.APPROVED

    @property
    def is_denied(self):
        return self.state == self.DENIED

    @property
    def is_done(self):
        return self.state == self.DONE

    @property
    def is_pending(self):
        return self.state == self.PENDING

    def set_done(self):
        self.state = self.DONE
        self.save()

    def __str__(self):
        return self.user_requester.get_full_name() + ' - ' + self.tutor_requested.get_full_name()


class Requesters(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    user_requester = models.ForeignKey(User, on_delete=models.CASCADE)

