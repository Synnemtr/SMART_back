# Generated by Django 3.2.20 on 2023-07-23 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20230723_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gamification_sub_type',
            field=models.IntegerField(blank=True, choices=[(0, 'Philanthropist'), (1, 'Socialiser'), (2, 'Free Spirit'), (3, 'Achiever'), (4, 'Disruptor'), (5, 'Player')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gamification_type',
            field=models.IntegerField(blank=True, choices=[(0, 'Philanthropist'), (1, 'Socialiser'), (2, 'Free Spirit'), (3, 'Achiever'), (4, 'Disruptor'), (5, 'Player')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='goal',
            field=models.IntegerField(blank=True, choices=[(1, 'Lose Weight'), (2, 'Build Muscle'), (3, 'Improve Endurance'), (4, 'Get Stronger'), (5, 'Stay Fit and Healthy'), (6, 'Other')]),
        ),
    ]
