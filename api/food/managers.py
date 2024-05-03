from django.db import models
from rest_framework import exceptions
import datetime
import pytz
from django.db import connection


class FoodManager(models.Manager):
    use_in_migrations = True

    def get_food_by_id(self, food_id):
        if not self.filter(id=food_id).exists():
            raise exceptions.ValidationError("Food with id {} does not exist".format(food_id))
        food = self.get(id=food_id)
        return food

    def get_foods(self):
        foods = self.all()
        return foods

    def create_food(self, **data):
        try:
            name = data.pop('name')
        except KeyError:
            raise exceptions.ValidationError("Name is required")
        food = self.create(name=name, **data)
        return food

    def update_food(self, food, **data):
        food.name = data.get('name', food.name)
        food.code = data.get('code', food.code)
        food.updated_at = datetime.datetime.now()
        food.save()
        return food

    def delete_food(self, food):
        food.delete()
        return food

    def add_macronutrient_to_food(self, food, macronutrient):
        food.macronutrients.add(macronutrient)
        return food

    def remove_macronutrient_from_food(self, food, macronutrient):
        food.macronutrients.remove(macronutrient)
        return food


class MacronutrientFoodManager(models.Manager):
    use_in_migrations = True

    def create_macronutrient_food(self, **data):
        try:
            food = data.pop('food')
            macronutrient = data.pop('macronutrient')
            amount = data.pop('amount')
        except KeyError:
            raise exceptions.ValidationError("Food, macronutrient and amount are required")
        macronutrient_food = self.filter(food=food, macronutrient=macronutrient)
        if macronutrient_food.exists():
            raise exceptions.ValidationError("Food already has this macronutrient")
        macronutrient_food = self.create(food=food, macronutrient=macronutrient, amount=amount)
        return macronutrient_food

    def update_macronutrient_food(self, macronutrient_food, **data):
        macronutrient_food.food = data.get('food', macronutrient_food.food)
        macronutrient_food.macronutrient = data.get('macronutrient', macronutrient_food.macronutrient)
        macronutrient_food.amount = data.get('amount', macronutrient_food.amount)
        macronutrient_food.save()
        return macronutrient_food

    def delete_macronutrient_food(self, macronutrient_food):
        macronutrient_food.delete()
        return macronutrient_food

    def rank_food_by_calories(self):
        query = """
                SELECT food_food.id, food_food.name, food_food.code, SUM(food_macronutrientfood.amount * macronutrient_macronutrient.calories_per_gram) AS calories
                FROM food_food, food_macronutrientfood, macronutrient_macronutrient
                WHERE food_food.id = food_macronutrientfood.food_id AND food_macronutrientfood.macronutrient_id = macronutrient_macronutrient.id
                GROUP BY food_food.id, food_food.name, food_food.code
                ORDER BY calories DESC
                """
        with connection.cursor() as cursor:
            cursor.execute(query)
            foods = cursor.fetchall()
        label = ["id", "name", "code", "calories"]
        foods = [dict(zip(label, food)) for food in foods]
        return foods


class FoodIntakeManager(models.Manager):
    def get_food_taken_by_user_on_date(self, user, date=None):
        if date is not None:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            date_start = datetime.datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=pytz.utc)
            date_end = datetime.datetime(date.year, date.month, date.day, 23, 59, 59, tzinfo=pytz.utc)
            query = """
                SELECT food_food.name, food_food.code, food_foodintake.quantity, food_foodintake.date
                FROM food_food, food_foodintake
                WHERE food_food.id = food_foodintake.food_id AND food_foodintake.user_id = %s AND food_foodintake.date BETWEEN %s AND %s
                ORDER BY food_foodintake.date DESC
                """
            with connection.cursor() as cursor:
                cursor.execute(query, [user.id, date_start, date_end])
                food_intake = cursor.fetchall()
        else:
            query = """
                SELECT food_food.name, food_food.code, food_foodintake.quantity, food_foodintake.date
                FROM food_food, food_foodintake
                WHERE food_food.id = food_foodintake.food_id AND food_foodintake.user_id = %s
                ORDER BY food_foodintake.date DESC
                """
            with connection.cursor() as cursor:
                cursor.execute(query, [user.id])
                food_intake = cursor.fetchall()
        label = ["name", "code", "quantity", "date"]
        result = [dict(zip(label, food)) for food in food_intake]
        return result

    def create_food_intake(self, user, **data):
        try:
            food = data.pop('food')
            quantity = data.pop('quantity')
        except KeyError:
            raise exceptions.ValidationError("Food and quantity are required")
        food_intake = self.create(user=user, food=food, quantity=quantity)
        return food_intake

    def update_food_intake(self, food_intake, **data):
        food_intake.food = data.get('food', food_intake.food)
        food_intake.amount = data.get('quantity', food_intake.quantity)
        food_intake.date = data.get('date', food_intake.date)
        food_intake.save()
        return food_intake

    def delete_food_intake(self, food_intake):
        food_intake.delete()
        return food_intake

class PlannedFoodManager(models.Manager):

    def create_planned_food(self, user, **data):
        try:
            food = data.pop('food')
            quantity = data.pop('quantity')
        except KeyError:
            raise exceptions.ValidationError("Food and quantity are required")
        planned_food = self.create(user=user, food=food, quantity=quantity)
        return planned_food

    def update_planned_food(self, planned_food, **data):
        planned_food.food = data.get('food', planned_food.food)
        planned_food.amount = data.get('quantity', planned_food.quantity)
        planned_food.date = data.get('date', planned_food.date)
        planned_food.save()
        return planned_food

    def delete_planned_food(self, planned_food):
        planned_food.delete()
        return planned_food