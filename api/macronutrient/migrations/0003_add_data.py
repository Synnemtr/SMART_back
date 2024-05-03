from django.db import migrations


def add_data(apps, schema_editor):
    Macronutrient = apps.get_model('macronutrient', 'Macronutrient')
    macronutrients = [
        {'name': 'Protein', 'calories_per_gram': 4},
        {'name': 'Carbohydrate', 'calories_per_gram': 4},
        {'name': 'Fat', 'calories_per_gram': 9},
    ]
    for macronutrient in macronutrients:
        Macronutrient.objects.create_macronutrient(**macronutrient)


class Migration(migrations.Migration):

    dependencies = [
        ('macronutrient', '0002_auto_20230708_1739'),
    ]

    operations = [
        migrations.RunPython(add_data),
    ]
