from django.db import models
from Course.models import Course


# Create your models here.
class User(models.Model):
    """Model for the User"""
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    type = models.IntegerField()
    photo_profile = models.ImageField(default='_static/images/default.jpg', upload_to='images/')

    @property
    def get_full_name(self):
        return self.name + " " + self.lastname

    def is_student(self):
        return self.type == 1

    def is_tutor(self):
        return self.type == 2

    def is_admin(self):
        return self.type == 3

    def __str__(self):
        return f'{self.name} {self.lastname}, {self.type}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'User'



