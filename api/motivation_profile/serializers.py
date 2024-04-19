from rest_framework import serializers
from api.motivation_profile.models import MotivationProfile
from api.motivation_question.models import MotivationQuestion
from app.serializers import AnswerField


class MotivationAnswerSerializer(serializers.Serializer):
    data = serializers.ListField(
        child=AnswerField()
    )

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        list_answer_type = MotivationQuestion.objects.validate_form_answer(validated_data['data'])
        MotivationProfile.objects.add_scores_for_motivation_profile(user_id, list_answer_type)
        return validated_data


class MotivationProfileSerializer(serializers.Serializer):
    name = serializers.CharField()
    score = serializers.FloatField()
