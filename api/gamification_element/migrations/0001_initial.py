# Generated by Django 3.2.23 on 2024-04-29 08:12

import api.gamification_element.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GamificationElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('HEXAD_12', models.CharField(max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('user_impact', models.CharField(blank=True, choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], max_length=255, null=True)),
                ('SDI_impact', models.CharField(blank=True, choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], max_length=255, null=True)),
            ],
            options={
                'db_table': 'gamification_element',
                'ordering': ['id'],
            },
            managers=[
                ('objects', api.gamification_element.managers.GamificationElementManager()),
            ],
        ),
    ]
