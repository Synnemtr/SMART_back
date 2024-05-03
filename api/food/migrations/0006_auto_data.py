from django.db import migrations

def fill_food_data(apps, schema_editor):
    Food = apps.get_model('food', 'Food')
    
    # Sample data for foods
    foods_data = [
        {'name': 'Chicken Breast', 'code': 'chicken-breast', 'calories': 165, 'carbohydrates': 0, 'fat': 3.6, 'protein': 31},
        {'name': 'Brown Rice', 'code': 'brown-rice', 'calories': 216, 'carbohydrates': 45, 'fat': 2, 'protein': 5},
        {'name': 'Salmon', 'code': 'salmon', 'calories': 233, 'carbohydrates': 0, 'fat': 13, 'protein': 25},
        {'name': 'Banana', 'code': 'banana', 'calories': 105, 'carbohydrates': 27, 'fat': 0.4, 'protein': 1.3},
        {'name': 'Broccoli', 'code': 'broccoli', 'calories': 34, 'carbohydrates': 7, 'fat': 0.4, 'protein': 2.8},
        {'name': 'Whole Wheat Bread', 'code': 'whole-wheat-bread', 'calories': 69, 'carbohydrates': 13, 'fat': 1, 'protein': 3},
        {'name': 'Eggs', 'code': 'eggs', 'calories': 78, 'carbohydrates': 0.6, 'fat': 5, 'protein': 6},
        {'name': 'Spinach', 'code': 'spinach', 'calories': 23, 'carbohydrates': 3.6, 'fat': 0.4, 'protein': 2.9},
        {'name': 'Apple', 'code': 'apple', 'calories': 95, 'carbohydrates': 25, 'fat': 0.3, 'protein': 0.5},
        {'name': 'Greek Yogurt', 'code': 'greek-yogurt', 'calories': 100, 'carbohydrates': 3.9, 'fat': 0, 'protein': 10},
        {'name': 'Almonds', 'code': 'almonds', 'calories': 576, 'carbohydrates': 21, 'fat': 49, 'protein': 21},
        {'name': 'Oatmeal', 'code': 'oatmeal', 'calories': 150, 'carbohydrates': 27, 'fat': 2.5, 'protein': 5},
        {'name': 'Cottage Cheese', 'code': 'cottage-cheese', 'calories': 98, 'carbohydrates': 3.4, 'fat': 4.3, 'protein': 11},
        {'name': 'Carrots', 'code': 'carrots', 'calories': 41, 'carbohydrates': 10, 'fat': 0.2, 'protein': 0.9},
        {'name': 'Peanut Butter', 'code': 'peanut-butter', 'calories': 588, 'carbohydrates': 20, 'fat': 50, 'protein': 25},
        {'name': 'Quinoa', 'code': 'quinoa', 'calories': 222, 'carbohydrates': 39, 'fat': 3.6, 'protein': 8},
        {'name': 'Sweet Potato', 'code': 'sweet-potato', 'calories': 86, 'carbohydrates': 20, 'fat': 0.1, 'protein': 1.6},
        {'name': 'Tuna', 'code': 'tuna', 'calories': 184, 'carbohydrates': 0, 'fat': 0.8, 'protein': 40},
        {'name': 'Milk', 'code': 'milk', 'calories': 42, 'carbohydrates': 5, 'fat': 1, 'protein': 3},
        {'name': 'Lentils', 'code': 'lentils', 'calories': 230, 'carbohydrates': 39, 'fat': 0.7, 'protein': 18},
    ]

    
    for data in foods_data:
        Food.objects.create(**data)

def remove_food_data(apps, schema_editor):
    # If needed, you can add a reverse operation to remove the data.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('food', '0005_auto_20230723_1132'),
    ]

    operations = [
        migrations.RunPython(fill_food_data, remove_food_data),
    ]
