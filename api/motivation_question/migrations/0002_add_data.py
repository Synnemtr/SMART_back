from django.db import migrations


def add_data(apps, schema_editor):
    MotivationQuestion = apps.get_model('motivation_question', 'MotivationQuestion')
    Motivation = apps.get_model('motivation', 'Motivation')
    motivation_questions = [
        {'question': 'It is fun to create meals that are good for my health',
            'motivation': Motivation.objects.get(name='Intrinsic motivation')},
        {'question': 'I like to find new ways to create meals that are good for my health',
            'motivation': Motivation.objects.get(name='Intrinsic motivation')},
        {'question': 'I take pleasure in fixing healthy meals',
            'motivation': Motivation.objects.get(name='Intrinsic motivation')},
        {'question': 'For the satisfaction of eating healthy',
            'motivation': Motivation.objects.get(name='Intrinsic motivation')},
        {'question': 'Eating healthy is an integral part of my life',
            'motivation': Motivation.objects.get(name='Integrated regulation')},
        {'question': 'Eating healthy is part of the way I have chosen to live my life',
            'motivation': Motivation.objects.get(name='Integrated regulation')},
        {'question': 'Regulating my eating behaviors has become a fundamental part of who I am',
            'motivation': Motivation.objects.get(name='Integrated regulation')},
        {'question': 'Eating healthy is congruent with other important aspects of my life',
             'motivation': Motivation.objects.get(name='Integrated regulation')},
        {'question': 'I believe it will eventually allow me to feel better',
                'motivation': Motivation.objects.get(name='Identified regulation')},
        {'question': 'I believe it’s a good thing I can do to feel better about myself in general',
                'motivation': Motivation.objects.get(name='Identified regulation')},
        {'question': 'It is a good idea to try to regulate my eating behaviors',
                'motivation': Motivation.objects.get(name='Identified regulation')},
        {'question': 'It is a way to ensure long-term health benefits',
                'motivation': Motivation.objects.get(name='Identified regulation')},
        {'question': 'I don’t want to be ashamed of how I look',
                'motivation': Motivation.objects.get(name='Introjected regulation')},
        {'question': 'I feel I must absolutely be thin',
                'motivation': Motivation.objects.get(name='Introjected regulation')},
        {'question': 'I would feel ashamed of myself if I was not eating healthy',
                'motivation': Motivation.objects.get(name='Introjected regulation')},
        {'question': 'I would be humiliated I was not in control of my eating behaviors',
                'motivation': Motivation.objects.get(name='Introjected regulation')},
        {'question': 'Other people close to me insist that I do',
                'motivation': Motivation.objects.get(name='External regulation')},
        {'question': 'Other people close to me will be upset if I don’t',
                'motivation': Motivation.objects.get(name='External regulation')},
        {'question': 'People around me nag me to do it',
                'motivation': Motivation.objects.get(name='External regulation')},
        {'question': 'It is expected of me',
                'motivation': Motivation.objects.get(name='External regulation')},
        {'question': 'I don’t really know. I truly have the impression that I’m wasting my time trying to regulate my eating behaviors',
                'motivation': Motivation.objects.get(name='Amotivation')},
        {'question': 'I don’t know why I bother',
                'motivation': Motivation.objects.get(name='Amotivation')},
        {'question': 'I can’t really see what I’m getting out of it',
                'motivation': Motivation.objects.get(name='Amotivation')},
        {'question': 'I don’t know. I can’t see how my efforts to eat healthy are helping my health situation',
                'motivation': Motivation.objects.get(name='Amotivation')}
    ]

    for motivation_question in motivation_questions:
        MotivationQuestion.objects.create_motivation_question(**motivation_question)


class Migration(migrations.Migration):

            dependencies = [
                ('motivation_question', '0001_initial'),
                ('motivation', '0002_add_data')
            ]

            operations = [
                migrations.RunPython(add_data),
            ]
