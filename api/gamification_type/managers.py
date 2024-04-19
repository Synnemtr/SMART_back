from rest_framework import exceptions
from django.db import models
import datetime


class GamificationTypeManager(models.Manager):
    use_in_migrations = True

    def validate_data(self, type_id):
        if not self.filter(id=type_id).exists():
            raise exceptions.ValidationError("Gamification type with id {} does not exist".format(type_id))

    def create_gamification_type(self, **data):
        try:
            name = data.pop('name')
        except KeyError:
            raise exceptions.ValidationError("Name is required")

        gamification_type = self.filter(name=name).first()
        if gamification_type:
            raise exceptions.ValidationError("Name is already taken")

        gamification_type = self.model(name=name, **data)
        gamification_type.save(using=self._db)
        return gamification_type

    def update_gamification_type(self, gamification_type, **data):
        gamification_type.name = data.get('name', gamification_type.name)
        gamification_type.description = data.get('description', gamification_type.description)
        gamification_type.updated_at = datetime.datetime.now()
        gamification_type.save()
        return gamification_type
