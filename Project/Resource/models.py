from django.db import models
from Tutorship.models import Tutorship


# Create your models here.
class Resource(models.Model):
    """Model for the Resource."""
    name = models.CharField(max_length=50)
    is_public = models.BooleanField(default=False)
    description = models.CharField(max_length=200)
    url = models.CharField(max_length=300)
    author = models.CharField(max_length=50)


class ResourceTutorship(models.Model):
    """Model for the relation between Resource and Tutorship."""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    tutorship = models.ForeignKey(Tutorship, on_delete=models.CASCADE, null=True)
