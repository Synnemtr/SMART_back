# Generated by Django 3.2.19 on 2023-07-08 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievement', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='achievement',
            table='achievement_achievement',
        ),
        migrations.AlterModelTable(
            name='userachievement',
            table='achievement_userachievement',
        ),
    ]
