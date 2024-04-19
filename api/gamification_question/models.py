from django.db import models
from app.models import BaseEntity
from api.gamification_question.managers import GamificationQuestionManager

RESPONSE_CHOICES = (
    ("Strong disagree", "1"),
    ("Disagree", "2"),
    ("Somewhat disagree", "3"),
    ("Neither", "4"),
    ("Somewhat agree", "5"),
    ("Agree", "6"),
    ("Strongly agree", "7"),
)


class GamificationQuestion(BaseEntity):
    class Meta:
        ordering = ["id"]
        db_table = "gamification_question"
    question = models.TextField(blank=False, null=False)
    gamification_type = models.ForeignKey('gamification_type.GamificationType', on_delete=models.CASCADE)
    objects = GamificationQuestionManager()
