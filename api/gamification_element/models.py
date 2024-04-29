from django.db import models
from api.gamification_element.managers import GamificationElementManager 
from app.models import BaseEntity

IMPACT_CHOICES = ( 
    ("LOW", "Low"), 
    ("MEDIUM", "Medium"), 
    ("HIGH", "High"), 
)

class GamificationElement(BaseEntity): 
    class Meta: 
        ordering = ["id"] 
        db_table = "gamification_element" 
    name = models.CharField(max_length=255, unique=True, blank=False, null=False) 
    HEXAD_12 = models.CharField(max_length=255, null=True) 
    description = models.TextField(blank=True, null=True) 
    user_impact = models.CharField(max_length=255, choices=IMPACT_CHOICES, blank=True, null=True) 
    SDI_impact = models.CharField(max_length=255, choices=IMPACT_CHOICES, blank=True, null=True) 
    objects = GamificationElementManager()