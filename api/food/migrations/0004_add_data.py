from django.db import migrations


def add_data(apps, schema_editor):
    Food = apps.get_model('food', 'Food')
    Macronutrient = apps.get_model('macronutrient', 'Macronutrient')
    MacronutrientFood = apps.get_model('food', 'MacronutrientFood')

    # Create foods
    foods = [
        {'name': 'Egg', 'code': 'egg-111'},
        {'name': 'Bacon', 'code': 'bacon-111'},
        {'name': 'Chicken Breast', 'code': 'chicken-breast-111'},
        {'name': 'Chicken Thigh', 'code': 'chicken-thigh-111'},
        {'name': 'Salad', 'code': 'salad-111'},
        {'name': 'Rice', 'code': 'rice-111'},
        {'name': 'Pasta', 'code': 'pasta-111'},
    ]
    for food in foods:
        Food.objects.create_food(**food)

    # Create macronutrients in foods
    data = [
        {'food': Food.objects.get(name='Egg'), 'macronutrient': Macronutrient.objects.get(name='Protein'),
         'amount': 6},
        {'food': Food.objects.get(name='Egg'), 'macronutrient': Macronutrient.objects.get(name='Fat'),
            'amount': 5},
        {'food': Food.objects.get(name='Bacon'), 'macronutrient': Macronutrient.objects.get(name='Protein'),
            'amount': 3},
        {'food': Food.objects.get(name='Bacon'), 'macronutrient': Macronutrient.objects.get(name='Fat'),
            'amount': 5},
        {'food': Food.objects.get(name='Chicken Breast'), 'macronutrient': Macronutrient.objects.get(name='Protein'),
            'amount': 20},
        {'food': Food.objects.get(name='Chicken Breast'), 'macronutrient': Macronutrient.objects.get(name='Fat'),
            'amount': 2},
        {'food': Food.objects.get(name='Chicken Thigh'), 'macronutrient': Macronutrient.objects.get(name='Protein'),
            'amount': 10},
        {'food': Food.objects.get(name='Chicken Thigh'), 'macronutrient': Macronutrient.objects.get(name='Fat'),
            'amount': 10},
        {'food': Food.objects.get(name='Salad'), 'macronutrient': Macronutrient.objects.get(name='Protein'),
            'amount': 1},
        {'food': Food.objects.get(name='Salad'), 'macronutrient': Macronutrient.objects.get(name='Carbohydrate'),
            'amount': 1},
        {'food': Food.objects.get(name='Salad'), 'macronutrient': Macronutrient.objects.get(name='Fat'),
            'amount': 1},
        {'food': Food.objects.get(name='Rice'), 'macronutrient': Macronutrient.objects.get(name='Carbohydrate'),
            'amount': 1},
        {'food': Food.objects.get(name='Pasta'), 'macronutrient': Macronutrient.objects.get(name='Carbohydrate'),
            'amount': 1},
    ]
    for datum in data:
        MacronutrientFood.objects.create_macronutrient_food(**datum)


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_auto_20230708_1733'),
        ('macronutrient', '0003_add_data'),
    ]

    operations = [
        migrations.RunPython(add_data),
    ]
