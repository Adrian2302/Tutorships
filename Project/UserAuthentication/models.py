from django.db import models


# Create your models here.
class User(models.Model):
    """Model for the User"""
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    type = models.CharField(max_length=10)
    photo_profile = models.CharField(max_length=300)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'User'
