from django.db import models
from api.gamification_pointsystem.managers import GamificationPointsystemManager
from app.models import BaseEntity


class GamificationPointsystem(BaseEntity):
    class Meta:
        ordering = ["id"]
        db_table = "gamification_pointsystem"
    element_name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)
    objects = GamificationPointsystemManager()
