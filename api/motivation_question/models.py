from django.db import models
from app.models import BaseEntity
from api.motivation_question.managers import MotivationQuestionManager


class MotivationQuestion(BaseEntity):
    question = models.CharField(max_length=255, unique=True, blank=False, null=False)
    motivation = models.ForeignKey('motivation.Motivation', on_delete=models.CASCADE)
    objects = MotivationQuestionManager()

    class Meta:
        db_table = 'motivation_question'
        ordering = ['id']

    def __str__(self):
        return self.question
