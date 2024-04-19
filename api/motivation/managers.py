from rest_framework import exceptions
from django.db import models
import datetime


class MotivationManager(models.Manager):
    use_in_migrations = True

    def create_motivation(self, **data):
        try:
            name = data.pop('name')
        except KeyError:
            raise exceptions.ValidationError("Name is required")

        motivation = self.filter(name=name).first()
        if motivation:
            raise exceptions.ValidationError("Name is already taken")

        motivation = self.model(name=name, **data)
        motivation.save(using=self._db)
        return motivation

    def update_motivation(self, motivation, **data):
        motivation.name = data.get('name', motivation.name)
        motivation.updated_at = datetime.datetime.now()
        motivation.save()
        return motivation

    def delete_motivation(self, motivation):
        motivation.delete()
        return True