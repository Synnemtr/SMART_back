# Generated by Django 3.2.23 on 2024-03-19 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_auto_20240315_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='HEXAD_12_sub_type',
            field=models.IntegerField(blank=True, choices=[(0, 'Philanthropist'), (1, 'Socialiser'), (2, 'Free Spirit'), (3, 'Achiever'), (4, 'Disruptor'), (5, 'Player')], null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='HEXAD_12_type',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='motivation_type',
            field=models.IntegerField(blank=True, choices=[(0, 'Non-Regulation'), (1, 'External Regulation'), (2, 'Introjected Regulation'), (3, 'Identified Regulation'), (4, 'Integrated Regulation'), (5, 'Intrinsic Motivation')], null=True),
        ),
    ]