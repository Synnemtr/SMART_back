from django.db import migrations


def add_data(apps, schema_editor):
    GamificationType = apps.get_model('gamification_type', 'GamificationType')
    hexadTypes = [
        {'name': 'Philanthropist', 'description': 'Philanthropists are people who engage in philanthropy; that is, they donate their time, money, and/or reputation to charitable causes. Philanthropy is a combination of two Greek words, philos, meaning love, and anthropos, meaning human beings, thus philanthropy is giving love for humanity.'},
        {'name': 'Socializer', 'description': 'Socializers are people who engage in socialization; that is, they interact with other people. Socialization is a combination of two Greek words, social, meaning companionship, and ization, meaning the process of making. Thus, socialization is the process of making companionship.'},
        {'name': 'Free Spirit', 'description': 'Free Spirits are people who engage in free spirit; that is, they are free from society. Free spirit is a combination of two Greek words, free, meaning freedom, and spirit, meaning soul, thus free spirit is the freedom of the soul.'},
        {'name': 'Achiever', 'description': 'Achievers are people who engage in achievement; that is, they accomplish goals. Achievement is a combination of two Greek words, achieve, meaning to accomplish, and ment, meaning the result of, thus achievement is the result of accomplishing.'},
        {'name': 'Disruptor', 'description': 'Disruptors are people who engage in disruption; that is, they interrupt the normal course. Disruption is a combination of two Greek words, dis, meaning not, and rupt, meaning break, thus disruption is the act of not breaking.'},
        {'name': 'Player', 'description': 'Players are people who engage in play; that is, they have fun. Play is a combination of two Greek words, ple, meaning pleasure, and ay, meaning the act of, thus play is the act of pleasure.'},
    ]
    for hexadType in hexadTypes:
        GamificationType.objects.create_gamification_type(**hexadType)


class Migration(migrations.Migration):

        dependencies = [
            ('gamification_type', '0001_initial'),
        ]

        operations = [
            migrations.RunPython(add_data),
        ]
