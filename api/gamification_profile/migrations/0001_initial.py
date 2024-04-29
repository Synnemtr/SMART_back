# Generated by Django 3.2.19 on 2023-07-19 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0002_auto_20230708_1733'),
        ('gamification_type', '0002_add_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='GamificationProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('gamification_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification_type.gamificationtype')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.profile')),
            ],
            options={
                'db_table': 'user_gamification_profile',
            },
        ),
    ]