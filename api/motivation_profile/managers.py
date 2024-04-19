from rest_framework import exceptions
from django.db import models, connection
import pandas as pd


class MotivationProfileManager(models.Manager):
    def create_motivation_profile(self, **data):
        try:
            profile_id = data.pop('profile_id')
            motivation_id = data.pop('motivation_id')
            score = data.pop('score')
        except KeyError:
            raise exceptions.ValidationError("Profile_id, motivation_id and score_id are required")
        motivation_profile = self.model(
            profile_id=profile_id,
            motivation_id=motivation_id,
            score=score
        )
        motivation_profile.save(using=self._db)
        return motivation_profile

    def update_motivation_profile(self, motivation_profile, **data):
        motivation_profile.score = data.get('score', motivation_profile.score)
        motivation_profile.save()
        return motivation_profile

    def delete_motivation_profile(self, motivation_profile):
        motivation_profile.delete()
        return motivation_profile

    def add_scores_for_motivation_profile(self, profile_id, list_answer_type):
        df = pd.DataFrame(list_answer_type)
        df = df.groupby(['motivation_id']).mean()
        df = df.reset_index()
        for index, row in df.iterrows():
            motivation_id = row['motivation_id']
            score = row['score']
            motivation_profile = self.filter(profile_id=profile_id, motivation_id=motivation_id).first()
            if motivation_profile is None:
                self.create_motivation_profile(
                    profile_id=profile_id,
                    motivation_id=motivation_id,
                    score=score
                )
            else:
                motivation_profile.score = score
                motivation_profile.save()

    def get_answer_by_profile_id(self, profile_id):
        if not self.filter(profile_id=profile_id).exists():
            raise exceptions.ValidationError("Answers with profile with id {} do not exist".format(profile_id))
        query = """
        SELECT motivation.name, user_motivation_profile.score
        FROM user_motivation_profile, motivation
        WHERE user_motivation_profile.motivation_id = motivation.id AND user_motivation_profile.profile_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [profile_id])
            profiles = cursor.fetchall()
        labels = ['name', 'score']
        result = [dict(zip(labels, profile)) for profile in profiles]
        return result
