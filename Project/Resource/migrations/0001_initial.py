# Generated by Django 3.2.8 on 2021-10-20 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('is_public', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=300)),
                ('author', models.CharField(max_length=50)),
            ],
        ),
    ]
