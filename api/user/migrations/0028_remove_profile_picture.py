# Generated by Django 3.2.23 on 2024-04-30 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_profile_goal_progress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='picture',
        ),
    ]
