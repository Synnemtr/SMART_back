from django.db import models
from api.gamification_profile.managers import GamificationProfileManager


class GamificationProfile(models.Model):
    class Meta:
        db_table = "user_gamification_profile"

    profile = models.ForeignKey('user.Profile', on_delete=models.CASCADE)
    gamification_type = models.ForeignKey('gamification_type.GamificationType', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)  # 2 - 14
    objects = GamificationProfileManager()
