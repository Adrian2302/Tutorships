# Generated by Django 3.2.5 on 2022-07-15 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAuthentication', '0004_alter_user_photo_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo_profile',
            field=models.ImageField(default='_static/images/default.jpg', upload_to=''),
        ),
    ]
