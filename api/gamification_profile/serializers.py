from rest_framework import serializers
from api.gamification_profile.models import GamificationProfile
from api.gamification_question.models import GamificationQuestion
from app.serializers import AnswerField


class GamificationAnswerSerializer(serializers.Serializer):
    data = serializers.ListField(
        child=AnswerField()
    )

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        list_answer_type = GamificationQuestion.objects.validate_form_answer(validated_data['data'])
        GamificationProfile.objects.add_scores_for_gamification_profile(user_id, list_answer_type)
        return validated_data


# class GamificationProfileSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     description = serializers.CharField()
#     score = serializers.IntegerField()

class GamificationProfileSerializer(serializers.Serializer):
    profile_id = serializers.IntegerField()
    gamification_type_id = serializers.IntegerField()
    score = serializers.IntegerField()