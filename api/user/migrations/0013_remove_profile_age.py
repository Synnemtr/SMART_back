# Generated by Django 3.2.23 on 2024-03-08 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_profile_date_of_birth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='age',
        ),
    ]
