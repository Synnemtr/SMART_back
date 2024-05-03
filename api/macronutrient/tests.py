from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from api.user.models import User


class MacronutrientTestCase(APITestCase):
    def setUp(self) -> None:
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

    def test_add_macronutrient_success(self):
        macronutrient_data = {
            "name": "Protein",
            "calories_per_gram": 4
        }
        response = self.client.post('/api/v1/macronutrients/', macronutrient_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
