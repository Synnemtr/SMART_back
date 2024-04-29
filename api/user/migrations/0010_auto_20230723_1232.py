# Generated by Django 3.2.20 on 2023-07-23 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20230723_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='training_per_week',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(blank=True, choices=[('MAN', 'Man'), ('WOMAN', 'Woman'), ('OTHER', 'Other')], max_length=255, null=True),
        ),
    ]