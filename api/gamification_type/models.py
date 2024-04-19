from django.db import models
from api.gamification_type.managers import GamificationTypeManager
from app.models import BaseEntity


class GamificationType(BaseEntity):
    class Meta:
        ordering = ["id"]
        db_table = "gamification_type"
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    objects = GamificationTypeManager()
