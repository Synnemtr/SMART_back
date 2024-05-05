from rest_framework import exceptions
from django.db import models
from django.db.models import Avg
from collections import defaultdict
import random


class RecommenderRatingManager(models.Manager):

    def create_rating(self, **data):
        required_keys = ["user_id", "game_element_id", "rating"]
        missing_keys = [key for key in required_keys if key not in data]

        if missing_keys:
            raise exceptions.ValidationError(f"Missing required keys: {', '.join(missing_keys)}")

        user_id = data.pop("user_id")
        game_element_id = data.pop("game_element_id")
        rating = data.pop("rating")
        if not (0 <= rating <= 5):
            raise exceptions.ValidationError("Rating must be between 0 and 5.")

        new_rating = self.model(
            user_id=user_id,
            game_element_id=game_element_id,
            rating=rating
        )
        new_rating.save(using=self._db)
        return new_rating

    def get_user_item_matrix(self):
        user_item_matrix = defaultdict(dict)

        for rating in self.all():
            user_item_matrix[rating.user_id][rating.game_element_id] = rating.rating

        return user_item_matrix

    def get_ratings_by_user(self, user_id):
        return self.filter(user_id=user_id).values('game_element_id', 'rank')

    def get_avg_rating(self, game_element_id):
        result = self.filter(game_element_id=game_element_id).aggregate(avg_rating=Avg("rating"))
        return result["avg_rating"]