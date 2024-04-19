from django.db import migrations


def add_data(apps, schema_editor):
    GamificationQuestion = apps.get_model('gamification_question', 'GamificationQuestion')
    GamificationType = apps.get_model('gamification_type', 'GamificationType')
    gamificationQuestions = [
        {'question': 'Rewards are a great way to motivate me', 'gamification_type': GamificationType.objects.get(name='Philanthropist')},
        {'question': 'It is important to me to follow my own path', 'gamification_type': GamificationType.objects.get(name='Philanthropist')},
        {'question': 'It makes me happy if I am able to help others', 'gamification_type': GamificationType.objects.get(name='Socializer')},
        {'question': 'I dislike following rules', 'gamification_type': GamificationType.objects.get(name='Socializer')},
        {'question': 'I see myself as a rebel', 'gamification_type': GamificationType.objects.get(name='Free Spirit')},
        {'question': 'I like to be in control of my own destiny', 'gamification_type': GamificationType.objects.get(name='Free Spirit')},
        {'question': 'I like mastering difficult tasks', 'gamification_type': GamificationType.objects.get(name='Achiever')},
        {'question': 'I enjoy emerging victorious out of difficult circumstances', 'gamification_type': GamificationType.objects.get(name='Achiever')},
        {'question': 'The well-being of others is important to me', 'gamification_type': GamificationType.objects.get(name='Disruptor')},
        {'question': 'I enjoy group activities', 'gamification_type': GamificationType.objects.get(name='Disruptor')},
        {'question': 'Being independent is important to me', 'gamification_type': GamificationType.objects.get(name='Player')},
        {'question': 'I like being part of a team', 'gamification_type': GamificationType.objects.get(name='Player')}
    ]

    for gamificationQuestion in gamificationQuestions:
        GamificationQuestion.objects.create_gamification_question(**gamificationQuestion)


class Migration(migrations.Migration):

            dependencies = [
                ('gamification_question', '0001_initial'),
                ('gamification_type', '0002_add_data'),
            ]

            operations = [
                migrations.RunPython(add_data),
            ]