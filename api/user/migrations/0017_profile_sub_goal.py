# Generated by Django 3.2.23 on 2024-03-09 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_alter_profile_hexad_12_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='sub_goal',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]