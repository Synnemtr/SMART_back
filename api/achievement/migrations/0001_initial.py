# Generated by Django 3.2.19 on 2023-07-05 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('threshold', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_earned', models.DateTimeField(auto_now_add=True)),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='achievement.achievement')),
            ],
        ),
    ]
