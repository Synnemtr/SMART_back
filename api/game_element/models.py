from django.db import models
from api.game_element.managers import GameElementManager 
from app.models import BaseEntity

IMPACT_CHOICES = ( 
    ("LOW", "Low"), 
    ("MEDIUM", "Medium"), 
    ("HIGH", "High"), 
)

class GameElement(BaseEntity): 
    class Meta: 
        ordering = ["id"] 
        db_table = "game_element" 
    name = models.CharField(max_length=255, unique=True, blank=False, null=False) 
    HEXAD_12 = models.CharField(max_length=255, null=True) 
    description = models.TextField(blank=True, null=True) 
    user_impact = models.CharField(max_length=255, choices=IMPACT_CHOICES, blank=True, null=True) 
    SDI_impact = models.CharField(max_length=255, choices=IMPACT_CHOICES, blank=True, null=True) 
    objects = GameElementManager()