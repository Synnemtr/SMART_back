from rest_framework import exceptions
from django.db import models
import datetime


class GameElementManager(models.Manager):
    use_in_migrations = True

    def validate_data(self, type_id):
        if not self.filter(id=type_id).exists():
            raise exceptions.ValidationError("Gamification type with id {} does not exist".format(type_id))

    def create_game_element(self, **data):
        try:
            name = data.pop('name')
        except KeyError:
            raise exceptions.ValidationError("Name is required")

        game_element = self.filter(name=name).first()
        if game_element:
            raise exceptions.ValidationError("Name is already taken")

        game_element = self.model(name=name, **data)
        game_element.save(using=self._db)
        return game_element

    def update_game_element(self, game_element, **data):
        game_element.name = data.get('name', game_element.name)
        game_element.description = data.get('description', game_element.description)
        game_element.updated_at = datetime.datetime.now()
        game_element.save()
        return game_element

    def delete_game_element(self, game_element):
        game_element.delete()
        return game_element