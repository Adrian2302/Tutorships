# Generated by Django 3.2.8 on 2021-10-30 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Tutorship', '0001_initial'),
        ('UserAuthentication', '0002_tutorcourse'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_requesters', models.IntegerField(default=0)),
                ('state', models.CharField(choices=[('PN', 'Pendiente'), ('AP', 'Aprobada'), ('DD', 'Rechazada'), ('DN', 'Realizada')], default='PN', max_length=2)),
                ('meeting_type', models.CharField(choices=[('ZO', 'Zoom'), ('DI', 'Discord'), ('ME', 'Meetup'), ('MT', 'Microsoft Teams'), ('PL', 'Lugar físico')], default='ZO', max_length=2)),
                ('tutor_comment', models.TextField()),
                ('student_comment', models.TextField()),
                ('date_start', models.DateTimeField(auto_now_add=True)),
                ('date_end', models.DateTimeField()),
                ('date_request', models.DateTimeField(auto_now_add=True)),
                ('date_resolution', models.DateTimeField()),
                ('tutorship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tutorship.tutorship')),
                ('user_requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_requester', to='UserAuthentication.user')),
            ],
        ),
        migrations.CreateModel(
            name='Requesters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.request')),
                ('user_requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserAuthentication.user')),
            ],
        ),
    ]
