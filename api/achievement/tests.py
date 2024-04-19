from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from api.user.models import User
from api.achievement.models import Achievement, UserAchievement


class AchievementTestCase(APITestCase):
    def setUp(self) -> None:
        user_data = {
            "username": "panh.hu"
        }
        user = User.objects.create_user(**user_data)
        # Create token
        client = APIClient()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        client.force_authenticate(user=user)
        self.client = client

    def test_get_all_achievements_success(self):
        response = self.client.get('/api/v1/achievements/')
        self.assertEqual(response.status_code, 200)

    def test_add_achievement_failed(self):
        achievement_data = {
            "name": "Achievement 1",
            "description": "Description 1",
            "threshold": 10
        }
        response = self.client.post('/api/v1/achievements/', achievement_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AchievementTestCase2(APITestCase):
    @classmethod
    def setUpTestData(cls):
        achievement = {
            "name": "Achievement 1",
            "description": "Description 1",
            "threshold": 10
        }
        Achievement.objects.create_achievement(**achievement)

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

    def test_add_achievement_success(self):
        achievement_data = {
            "name": "Achievement 2",
            "description": "Description 1",
            "threshold": 10
        }
        response = self.client.post('/api/v1/achievements/', achievement_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_achievement_no_name(self):
        achievement_data = {
            "threshold": 10
        }
        response = self.client.post('/api/v1/achievements/', achievement_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_achievement_duplicate_name(self):
        achievement_data = {
            "name": "Achievement 1",
            "description": "Description 1",
            "threshold": 10
        }
        response = self.client.post('/api/v1/achievements/', achievement_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAchievementTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        achievement = {
            "name": "Achievement 1",
            "description": "Description 1",
            "threshold": 10
        }
        achievement = Achievement.objects.create_achievement(**achievement)
        user_data = {
            "username": "user-1"
        }
        user = User.objects.create_user(**user_data)
        UserAchievement.objects.create_user_achievement(user_id=user.id, achievement_id=achievement.id)
        Achievement.objects.add_user_to_achievement(user=user, achievement=achievement)

    def setUp(self) -> None:
        user = User.objects.get(username='user-1')
        # Create token
        client = APIClient()
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        client.force_authenticate(user=user)
        self.client = client

    def test_get_user_achievement_success(self):
        response = self.client.get('/api/v1/achievements/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_add_user_achievement_success(self):
        achievement_data = {
            "name": "Achievement 2",
            "description": "Description 1",
            "threshold": 10
        }
        achievement = Achievement.objects.create_achievement(**achievement_data)
        response = self.client.post('/api/v1/achievements/list/user/', {'achievement_id': achievement.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_user_achievement_duplicate(self):
        achievement = Achievement.objects.get(name='Achievement 1')
        response = self.client.post('/api/v1/achievements/list/user/', {'achievement_id': achievement.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user_achievement_success(self):
        achievement = Achievement.objects.get(name='Achievement 1')
        user = User.objects.get(username='user-1')
        user_achievement = UserAchievement.objects.get(user_id=user.id, achievement_id=achievement.id)
        response = self.client.delete(f'/api/v1/achievements/list/user/{user_achievement.id}')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
