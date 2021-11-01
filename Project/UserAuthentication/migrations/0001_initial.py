# Generated by Django 3.2.8 on 2021-11-01 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('type', models.IntegerField()),
                ('photo_profile', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='TutorCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Course.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserAuthentication.user')),
            ],
        ),
    ]
