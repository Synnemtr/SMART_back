from django.db import models
from api.motivation_profile.managers import MotivationProfileManager


class MotivationProfile(models.Model):
    class Meta:
        db_table = "user_motivation_profile"

    profile = models.ForeignKey('user.Profile', on_delete=models.CASCADE)
    motivation = models.ForeignKey('motivation.Motivation', on_delete=models.CASCADE)
    score = models.FloatField(default=0)  # 1 - 7
    objects = MotivationProfileManager()
