# Generated by Django 3.2.8 on 2021-10-29 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0002_auto_20211029_0641'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tutor',
            old_name='type_mode',
            new_name='modality_type',
        ),
        migrations.RenameField(
            model_name='tutor',
            old_name='session',
            new_name='session_type',
        ),
        migrations.AddField(
            model_name='tutor',
            name='payment_type',
            field=models.CharField(default='Ninguno', max_length=20),
        ),
    ]
