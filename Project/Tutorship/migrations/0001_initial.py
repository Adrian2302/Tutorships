# Generated by Django 3.2.8 on 2021-10-27 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Course', '0001_initial'),
        ('UserAuthentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tutorship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_people', models.IntegerField()),
                ('state', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('name', models.CharField(max_length=80)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='TutorshipCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Course.course')),
                ('tutorship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tutorship.tutorship')),
            ],
        ),
        migrations.CreateModel(
            name='TutorshipAvailableSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserAuthentication.user')),
            ],
        ),
    ]
