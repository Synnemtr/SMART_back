from django.db import models
from app.models import BaseEntity
from api.game_element_quiz.managers import GameQuizManager


class GameQuiz(BaseEntity):
    class Meta:
        ordering = ["id"]
        db_table = "game_element_quiz"

    question = models.TextField(blank=False, null=False)
    option_one = models.CharField(max_length=255, blank=False, null=False, default='')
    option_two = models.CharField(max_length=255, blank=False, null=False, default='')
    option_three = models.CharField(max_length=255, blank=False, null=False, default='')
    option_four = models.CharField(max_length=255, blank=False, null=False, default='')
    correct_answer = models.CharField(max_length=255, blank=False, null=False, default='')
    objects = GameQuizManager()
