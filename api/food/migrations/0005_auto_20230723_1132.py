# Generated by Django 3.2.20 on 2023-07-23 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_add_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='calories',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='food',
            name='carbohydrates',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='food',
            name='fat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='food',
            name='protein',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
