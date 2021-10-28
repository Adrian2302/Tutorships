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
    photo_profile = models.CharField(max_length=300)

    def is_student(self):
        return self.type == 1

    def is_tutor(self):
        return self.type == 2

    def is_admin(self):
        return self.type == 3

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'User'


class TutorCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

