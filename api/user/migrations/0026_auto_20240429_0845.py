# Generated by Django 3.2.23 on 2024-04-29 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_alter_profile_current_streak'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='HEXAD_12_sub_type',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='HEXAD_12_type',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='current_streak',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='motivation_type',
        ),
    ]
