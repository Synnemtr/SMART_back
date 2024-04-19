from rest_framework import serializers
from api.motivation_question.models import MotivationQuestion


class MotivationQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotivationQuestion
        fields = ['id', 'question', 'motivation']
        read_only_fields = ('id',)

    def create(self, validated_data):
        return MotivationQuestion.objects.create_motivation_question(**validated_data)

    def update(self, instance, validated_data):
        instance = MotivationQuestion.objects.update_motivation_question(instance, **validated_data)
        return instance
    