from django.db import models
from api.macronutrient.managers import MacronutrientManager
from app.models import BaseEntity


class Macronutrient(BaseEntity):
    class Meta:
        ordering = ('id',)
        db_table = 'macronutrient_macronutrient'

    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    calories_per_gram = models.IntegerField()
    objects = MacronutrientManager()

    def __str__(self):
        return self.name
