from app.models import BaseEntity
from django.db import models
from api.motivation.managers import MotivationManager


class Motivation(BaseEntity):
    class Meta:
        ordering = ["id"]
        db_table = "motivation"
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    objects = MotivationManager()
