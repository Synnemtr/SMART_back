from rest_framework import serializers
from api.gamification_question.models import GamificationQuestion


class GamificationQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamificationQuestion
        fields = ['id', 'question', 'gamification_type']
        read_only_fields = ('id',)

    def create(self, validated_data):
        return GamificationQuestion.objects.create_gamification_question(**validated_data)

    def update(self, instance, validated_data):
        instance = GamificationQuestion.objects.update_gamification_question(instance, **validated_data)
        return instance
    