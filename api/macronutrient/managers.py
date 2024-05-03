from django.db import models
from rest_framework import exceptions
import datetime


class MacronutrientManager(models.Manager):
    use_in_migrations = True

    def get_macronutrient_by_id(self, macronutrient_id):
        if not self.filter(id=macronutrient_id).exists():
            raise exceptions.ValidationError("Macronutrient with id {} does not exist".format(macronutrient_id))
        macronutrient = self.get(id=macronutrient_id)
        return macronutrient

    def get_macronutrient_by_name(self, name):
        macronutrient = self.filter(name=name).first()
        return macronutrient

    def get_macronutrients(self):
        macronutrients = self.all()
        return macronutrients

    def create_macronutrient(self, **data):
        try:
            name = data.pop('name')
        except KeyError:
            raise exceptions.ValidationError("Name is required")
        macronutrient = self.create(name=name, **data)
        return macronutrient

    def update_macronutrient(self, macronutrient, **data):
        macronutrient.name = data.get('name', macronutrient.name)
        macronutrient.calories_per_gram = data.get('calories_per_gram', macronutrient.calories_per_gram)
        macronutrient.updated_at = datetime.datetime.now()
        macronutrient.save()
        return macronutrient

    def delete_macronutrient(self, macronutrient):
        macronutrient.delete()
        return macronutrient
