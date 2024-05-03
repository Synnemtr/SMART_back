from django.db import models
from api.food.managers import FoodManager, MacronutrientFoodManager, FoodIntakeManager, PlannedFoodManager
from app.models import BaseEntity


class FoodIntake(models.Model):
    class Meta:
        unique_together = ('user', 'food', 'date')
        db_table = 'food_foodintake'

    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    food = models.ForeignKey('food.Food', on_delete=models.CASCADE)
    quantity = models.FloatField()
    date = models.DateTimeField(auto_now=True)
    objects = FoodIntakeManager()

    def __str__(self):
        return "{} - {}".format(self.user.username, self.food.name)

    def is_owner(self, user_id):
        return self.user.id == user_id
    
class PlannedFood(models.Model):
    class Meta:
        unique_together = ('user', 'food', 'date')
        db_table = 'food_plannedfood'

    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    food = models.ForeignKey('food.Food', on_delete=models.CASCADE)
    quantity = models.FloatField()
    date = models.DateTimeField(auto_now=True)
    objects = PlannedFoodManager()

    def __str__(self):
        return "{} - {}".format(self.user.username, self.food.name)

    def is_owner(self, user_id):
        return self.user.id == user_id


class Food(BaseEntity):
    class Meta:
        ordering = ('id',)
        db_table = 'food_food'

    name = models.CharField(max_length=255)
    macronutrients = models.ManyToManyField('macronutrient.Macronutrient', through='food.MacronutrientFood')
    code = models.CharField(max_length=255, null=True, blank=True, unique=True)
    calories = models.FloatField(blank=True, null=True)
    carbohydrates = models.FloatField(blank=True, null=True)
    fat = models.FloatField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)
    
    objects = FoodManager()

    def __str__(self):
        return self.name


class MacronutrientFood(models.Model):
    class Meta:
        unique_together = ('food', 'macronutrient')
        db_table = 'food_macronutrientfood'

    food = models.ForeignKey('food.Food', on_delete=models.CASCADE)
    macronutrient = models.ForeignKey('macronutrient.Macronutrient', on_delete=models.CASCADE)
    amount = models.FloatField(blank=False, null=False)
    objects = MacronutrientFoodManager()

    def __str__(self):
        return "{} - {}".format(self.food.name, self.macronutrient.name)
