# Generated by Django 3.2.23 on 2024-03-27 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_profile_current_streak'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='current_streak',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
