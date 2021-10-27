# Generated by Django 3.2.8 on 2021-10-26 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserAuthentication', '0001_initial'),
        ('Tutorship', '0002_coursetutorship_id_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorship',
            name='state',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='TutorAvailableSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserAuthentication.user')),
            ],
        ),
    ]
