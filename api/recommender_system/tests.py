from django.test import TestCase
from api.recommender_rating.models import Rating
from api.user.models import User
from api.game_element.models import GameElement

# Create your tests here.
class RecommenderRatingManagerTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=2)
        self.game_element1 = GameElement.objects.get(id=1)
        self.game_element2 = GameElement.objects.get(id=2)
        Rating.objects.create(id=1, rating=5, game_element=self.game_element1, user=self.user1)
        Rating.objects.create(id=2, rating=0, game_element=self.game_element2, user=self.user1)
        Rating.objects.create(id=3, rating=4, game_element=self.game_element1, user=self.user2)
        Rating.objects.create(id=4, rating=2, game_element=self.game_element2, user=self.user2)

    def test_get_ratings_by_user(self):
        ratings = Rating.objects.get_ratings_by_user(self.user1.id)
        self.assertEqual(ratings.count(), 2)

    def test_get_avg_rating(self):
        avg_rating = Rating.objects.get_avg_rating(self.game_element1.id)
        self.assertEqual(avg_rating, 4)