from django.db import models
from UserAuthentication.models import User
from datetime import datetime


# Create your models here.
class Room(models.Model):
    original_user_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='original_user_sender')
    original_user_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='original_user_receiver')


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user_sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_sent = models.DateTimeField(default=datetime.now, blank=True)


class MessageNotification(models.Model):
    """Model for the message notifications."""
    NEW_MESSAGE = 'NM'
    NEW_REPLY = 'NR'

    TYPES = (
        (NEW_MESSAGE, 'New Message'),
        (NEW_REPLY, 'New Reply'),
    )

    notification_type = models.CharField(max_length=2, choices=TYPES)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_to', null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_from', null=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=datetime.now)
    seen = models.BooleanField(default=False)

    def is_new_message(self):
        return self.notification_type == self.NEW_MESSAGE

    def is_new_reply(self):
        return self.notification_type == self.NEW_REPLY
