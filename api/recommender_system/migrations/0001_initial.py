# Generated by Django 3.2.23 on 2024-05-03 10:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('game_element', '0002_alter_gameelement_table'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommenderSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('recommended_items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_element.gameelement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'recommender_system',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
