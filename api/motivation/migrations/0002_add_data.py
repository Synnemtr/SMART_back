from django.db import migrations


def add_data(apps, schema_editor):
    Motivation = apps.get_model('motivation', 'Motivation')
    motivations = [
        {'name': 'Intrinsic motivation'},
        {'name': 'Integrated regulation'},
        {'name': 'Identified regulation'},
        {'name': 'Introjected regulation'},
        {'name': 'External regulation'},
        {'name': 'Amotivation'}
    ]

    for motivation in motivations:
        Motivation.objects.create_motivation(**motivation)


class Migration(migrations.Migration):

        dependencies = [
            ('motivation', '0001_initial'),
        ]

        operations = [
            migrations.RunPython(add_data),
        ]
