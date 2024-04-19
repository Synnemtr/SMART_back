from rest_framework import serializers


class AnswerField(serializers.DictField):
    question_id = serializers.IntegerField()
    score = serializers.IntegerField()
