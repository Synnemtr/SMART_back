# Generated by Django 3.2.20 on 2023-07-22 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20230708_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='goal',
            field=models.CharField(blank=True, choices=[(1, 'Lose Weight'), (2, 'Build Muscle'), (3, 'Improve Endurance'), (4, 'Get Stronger'), (5, 'Stay Fit and Healthy'), (6, 'Other')], max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='preferred_diet',
            field=models.CharField(choices=[('vegetarian', 'Vegetarian'), ('vegan', 'Vegan'), ('pescatarian', 'Pescatarian'), ('keto', 'Keto'), ('paleo', 'Paleo'), ('gluten_free', 'Gluten-Free')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='total_points',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='height',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='weight',
            field=models.FloatField(blank=True),
        ),
    ]
