from django.core.management.base import BaseCommand

from Course.models import Course
from Region.models import Regions
from UserAuthentication.models import User


def load_courses():
    Course.objects.all().delete()
    Course.objects.create(
        university='University of Pretoria',
        name='Introduction Computer Science',
        description='This is a course for the B.Sc. in Computer Science'
    )

    Course.objects.create(
        university='University of Vienna',
        name='Medicine',
        description='This is a course for Medicine'
    )

    Course.objects.create(
        university='University of Costa Rica',
        name='Mathematics',
        description='This is a course for Mathematics'
    )


class Command(BaseCommand):
    help = 'Loads data to the database'

    def handle(self, *args, **options):
        load_courses()
        self.stdout.write(self.style.SUCCESS('Successfully loaded data to models.'))