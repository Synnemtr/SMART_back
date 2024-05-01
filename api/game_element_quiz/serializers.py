from rest_framework import serializers
from api.game_element_quiz.models import GameQuiz

class GameQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameQuiz
        fields = ['id', 'question', 'option_one', 'option_two', 'option_three', 'option_four', 'correct_answer']
        read_only_fields = ('id',)

    def create(self, validated_data):
        return GameQuiz.objects.create_game_quiz(**validated_data)

    def update(self, instance, validated_data):
        instance = GameQuiz.objects.update_game_quiz(instance, **validated_data)
        return instance