from django.core.management.base import BaseCommand

from Course.models import Course
from Region.models import Regions
from Modality.models import Modality
from Payment.models import Payment
from Session.models import Session
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


def load_regions():
    Regions.objects.all().delete()
    Regions.objects.create(
        region_name='Heredia',
        country='Costa Rica'
    )
    Regions.objects.create(
        region_name='San Jose',
        country='Costa Rica'
    )
    Regions.objects.create(
        region_name='Cartago',
        country='Costa Rica'
    )
    Regions.objects.create(
        region_name='Puntarenas',
        country='Costa Rica'
    )
    Regions.objects.create(
        region_name='Alajuela',
        country='Costa Rica'
    )
    Regions.objects.create(
        region_name='Limón',
        country='Costa Rica'
    )
    Regions.objects.create(
        region_name='Guanacaste',
        country='Costa Rica'
    )


def load_payments():
    Payment.objects.all().delete()
    Payment.objects.create(
        name='PayPal',
        description='This is a payment method for PayPal'
    )
    Payment.objects.create(
        name='Credit Card',
        description='This is a payment method for Credit Card'
    )
    Payment.objects.create(
        name='Cash',
        description='This is a payment method for Cash'
    )


def load_sessions():
    Session.objects.all().delete()
    Session.objects.create(
        name='One-on-one',
        description='This is a session for one-on-one tutoring'
    )
    Session.objects.create(
        name='Group',
        description='This is a session for group tutoring'
    )


def load_modalities():
    Modality.objects.all().delete()
    Modality.objects.create(
        name='Online',
        description='This is a modality for online tutoring'
    )
    Modality.objects.create(
        name='In-person',
        description='This is a modality for in-person tutoring'
    )


class Command(BaseCommand):
    help = 'Loads data to the database'

    def handle(self, *args, **options):
        # load_courses()
        # load_regions()
        load_payments()
        load_sessions()
        load_modalities()
        self.stdout.write(self.style.SUCCESS('Successfully loaded data to models.'))