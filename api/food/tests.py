from rest_framework import exceptions
from rest_framework.test import APITestCase, APIClient
from api.macronutrient.models import Macronutrient
from api.food.models import Food, MacronutrientFood
from api.user.models import User
from rest_framework.authtoken.models import Token


class MacronutrientFoodTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        list_macronutrients = [
            {
                "name": "Protein",
                "calories_per_gram": 4
            },
            {
                "name": "Carbohydrate",
                "calories_per_gram": 4
            },
            {
                "name": "Fat",
                "calories_per_gram": 9
            },
            {
                "name": "Alcohol",
                "calories_per_gram": 7
            }
        ]
        for macronutrient in list_macronutrients:
            Macronutrient.objects.create_macronutrient(**macronutrient)
        egg = {
            "name": "Egg",
            "code": "egg-111"
        }
        Food.objects.create_food(**egg)
        cls.egg = Food.objects.get(name="Egg")
        protein = Macronutrient.objects.get(name="Protein")
        fat = Macronutrient.objects.get(name="Fat")
        carbohydrate = Macronutrient.objects.get(name="Carbohydrate")
        MacronutrientFood.objects.create_macronutrient_food(
            food=cls.egg,
            macronutrient=protein,
            amount=6.3
        )
        MacronutrientFood.objects.create_macronutrient_food(
            food=cls.egg,
            macronutrient=fat,
            amount=5.3
        )
        MacronutrientFood.objects.create_macronutrient_food(
            food=cls.egg,
            macronutrient=carbohydrate,
            amount=0.6
        )
        Food.objects.add_macronutrient_to_food(food=cls.egg, macronutrient=protein)
        Food.objects.add_macronutrient_to_food(food=cls.egg, macronutrient=fat)
        Food.objects.add_macronutrient_to_food(food=cls.egg, macronutrient=carbohydrate)

    def setUp(self):
        user_data = {
            "username": "admin"
        }
        user = User.objects.create_user(is_superuser=True, **user_data)
        # Create token
        client = APIClient()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        client.force_authenticate(user=user)
        self.client = client

    def test_add_macronutrient_to_food_duplicate(self):
        protein = Macronutrient.objects.get(name="Protein")

        response = self.client.post(f'/api/v1/foods/{self.egg.id}/macronutrients/', {
            "macronutrient": protein.id,
            "food": self.egg.id
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertRaises(exceptions.ValidationError)

    def test_delete_macronutrient_from_food(self):
        protein = Macronutrient.objects.get(name="Protein")
        response = self.client.delete(f'/api/v1/foods/{self.egg.id}/macronutrients/{protein.id}/')
        self.assertEqual(self.egg.macronutrients.count(), 2)
        self.assertEqual(response.status_code, 204)

    def test_create_macronutrient_food_success(self):
        alcohol = Macronutrient.objects.get(name="Alcohol")
        response = self.client.post(f'/api/v1/foods/{self.egg.id}/macronutrients/', {
            "macronutrient": alcohol.id,
            "food": self.egg.id,
            "amount": 0.1
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.egg.macronutrients.count(), 4)

    def test_update_macronutrient_food_success(self):
        protein = Macronutrient.objects.get(name="Protein")
        response = self.client.put(f'/api/v1/foods/{self.egg.id}/macronutrients/{protein.id}/', {
            "macronutrient": protein.id,
            "food": self.egg.id,
            "amount": 7.3
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.egg.macronutrients.count(), 3)

    def tearDown(self):
        MacronutrientFood.objects.all().delete()
        Food.objects.all().delete()
        Macronutrient.objects.all().delete()
