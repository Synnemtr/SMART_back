from rest_framework import exceptions
from django.db import models
import random
import operator
import numpy as np
from api.recommender_rating.models import Rating
from api.game_element.models import GameElement
from api.user.serializers import ProfileSerializer
from api.user.models import User, Profile


class RecommenderSystemManger(models.Manager):
    def calculate_cosine_similarity(self, user_ratings):
        user_rating_dict = {}
        for rating in user_ratings:
            user_rating_dict.setdefault(rating.user_id, {})[rating.game_element_id] = rating.rating

        user_ids = list(user_rating_dict.keys())
        similarity_matrix = np.zeros((len(user_ids), len(user_ids)))

        for i, user1 in enumerate(user_ids):
            for j, user2 in enumerate(user_ids):
                if i == j:
                    similarity_matrix[i, j] = 1
                else:
                    user1_ratings = user_rating_dict[user1]
                    user2_ratings = user_rating_dict[user2]

                    common_elements = set(user1_ratings.keys()) & set(user2_ratings.keys())
                    if common_elements:
            
                        user1_mean = np.mean(list(user1_ratings.values()))
                        user2_mean = np.mean(list(user2_ratings.values()))

                        user1_vector = np.array([user1_ratings[e] - user1_mean for e in common_elements])
                        user2_vector = np.array([user2_ratings[e] - user2_mean for e in common_elements])

                        dot_product = np.dot(user1_vector, user2_vector)
                        norm_user1 = np.linalg.norm(user1_vector)
                        norm_user2 = np.linalg.norm(user2_vector)

                        similarity_matrix[i, j] = dot_product / (norm_user1 * norm_user2)

        return similarity_matrix, user_ids

    
    def get_user_recommendations(self, user_id, top_n=3):
        try:
            user_obj = User.objects.get(id=user_id)
            profile_obj = Profile.objects.get(user=user_obj)
        except User.DoesNotExist:
            raise ValueError(f"User with id {user_id} does not exist.")
        except Profile.DoesNotExist:
            raise ValueError(f"Profile for user with id {user_id} does not exist.")

        profile_serializer = ProfileSerializer()
        user_hexad_type = profile_serializer.get_HEXAD_12_type(profile_obj)

        all_ratings = Rating.objects.all()
        all_ratings = list(filter(lambda rating: rating.rating != 0, all_ratings))
        similarity_matrix, user_ids = self.calculate_cosine_similarity(all_ratings)

        if user_id not in user_ids:
            return self.get_random_recommendation(user_id, top_n=top_n)

        user_index = user_ids.index(user_id)
        similar_users_indices = np.argsort(similarity_matrix[user_index])[::-1]
        similar_users_indices = [i for i in similar_users_indices if i != user_index]
        user_rating_dict = {rating.game_element_id: rating.rating for rating in all_ratings if rating.user_id == user_id}

        recommendations = {}
        for similar_user_index in similar_users_indices:
            similar_user_id = user_ids[similar_user_index]
            similar_user_ratings = [r for r in all_ratings if r.user_id == similar_user_id]

            for rating in similar_user_ratings:
                if rating.game_element_id not in user_rating_dict:
                    game_element = GameElement.objects.get(id=rating.game_element_id)
                    if user_hexad_type in game_element.HEXAD_12.split(', '):
                        recommendations[rating.game_element] = rating.rating

                        if len(recommendations) >= top_n:
                            break

            if len(recommendations) >= top_n:
                break

        if len(recommendations) == 0:
            return self.get_random_recommendation(user_id, top_n=top_n)

        sorted_recommendations = dict(sorted(recommendations.items(), key=lambda item: item[1], reverse=True))
        return sorted_recommendations
    
    def get_random_recommendation(self, user_id, top_n=1):
        try:
            user_obj = User.objects.get(id=user_id)
            profile_obj = Profile.objects.get(user=user_obj)
        except User.DoesNotExist:
            raise ValueError(f"User with id {user_id} does not exist.")
        except Profile.DoesNotExist:
            raise ValueError(f"Profile for user with id {user_id} does not exist.")

        profile_serializer = ProfileSerializer()
        user_hexad_type = profile_serializer.get_HEXAD_12_type(profile_obj)

        matching_elements = GameElement.objects.filter(HEXAD_12__contains=user_hexad_type)
        if len(matching_elements) < top_n:
            raise ValueError(f"Cannot generate {top_n} recommendations as there are only {len(matching_elements)} matching elements.")
        recommendations = random.sample(list(matching_elements), top_n)

        return recommendations