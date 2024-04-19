from rest_framework import exceptions
from django.db import models, connection
import pandas as pd


class GamificationProfileManager(models.Manager):
    def create_gamification_profile(self, **data):
        try:
            profile_id = data.pop('profile_id')
            gamification_type_id = data.pop('gamification_type_id')
            score = data.pop('score')
        except KeyError:
            raise exceptions.ValidationError("Profile_id, gamification_type_id and score are required")
        gamification_profile = self.model(
            profile_id=profile_id,
            gamification_type_id=gamification_type_id,
            score=score
        )
        gamification_profile.save(using=self._db)
        return gamification_profile

    def update_gamification_profile(self, gamification_profile, **data):
        gamification_profile.score = data.get('score', gamification_profile.score)
        gamification_profile.save()
        return gamification_profile

    def delete_gamification_profile(self, gamification_profile):
        gamification_profile.delete()
        return gamification_profile

    def add_scores_for_gamification_profile(self, profile_id, list_answer_type):
        df = pd.DataFrame(list_answer_type)
        df = df.groupby(['type_question_id']).sum()
        df = df.reset_index()
        for index, row in df.iterrows():
            gamification_type_id = row['type_question_id']
            score = row['score']
            gamification_profile = self.filter(profile_id=profile_id, gamification_type_id=gamification_type_id).first()
            if gamification_profile is None:
                self.create_gamification_profile(
                    profile_id=profile_id,
                    gamification_type_id=gamification_type_id,
                    score=score
                )
            else:
                gamification_profile.score = score
                gamification_profile.save()

    def get_answer_by_profile_id(self, profile_id):
        if not self.filter(profile_id=profile_id).exists():
            raise exceptions.ValidationError("Answers with profile with id {} do not exist".format(profile_id))
        query = """
        SELECT gamification_type.name, gamification_type.description, user_gamification_profile.score
        FROM user_gamification_profile, gamification_type
        WHERE user_gamification_profile.gamification_type_id = gamification_type.id AND user_gamification_profile.profile_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [profile_id])
            profiles = cursor.fetchall()
        labels = ['name', 'description', 'score']
        result = [dict(zip(labels, profile)) for profile in profiles]
        return result
    
    def get_all_answers(self):
        query = """
        SELECT DISTINCT user_gamification_profile.profile_id, gamification_type.id, user_gamification_profile.score
        FROM user_gamification_profile, gamification_type
        WHERE user_gamification_profile.gamification_type_id = gamification_type.id
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            profiles = cursor.fetchall()
        labels = ['profile_id', 'gamification_type_id', 'score']
        result = [dict(zip(labels, profile)) for profile in profiles]
        return result
