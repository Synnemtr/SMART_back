from rest_framework import exceptions
from django.db import models
import datetime


class GamificationPointsystemManager(models.Manager):
    use_in_migrations = True

    def validate_data(self, element_name):
        if not self.filter(element_name=element_name).exists():
            raise exceptions.ValidationError("Gamification point system with element name {} does not exist".format(element_name))

    def create_gamification_pointsystem(self, **data):
        try:
            element_name = data.pop('element_name')
        except KeyError:
            raise exceptions.ValidationError("Element name is required")

        gamification_pointsystem = self.filter(element_name=element_name).first()
        if gamification_pointsystem:
            raise exceptions.ValidationError("Element name is already taken")

        gamification_pointsystem = self.model(element_name=element_name, **data)
        gamification_pointsystem.save(using=self._db)
        return gamification_pointsystem

    def update_gamification_pointsystem(self, gamification_pointsystem, **data):
        gamification_pointsystem.element_name = data.get('element_name', gamification_pointsystem.element_name)
        gamification_pointsystem.description = data.get('description', gamification_pointsystem.description)
        gamification_pointsystem.point = data.get('point', gamification_pointsystem.point)
        gamification_pointsystem.updated_at = datetime.datetime.now()
        gamification_pointsystem.save()
        return gamification_pointsystem