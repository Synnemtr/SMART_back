from django.db import models
from api.achievement.managers import AchievementManager, UserAchievementManager, ActiveUserAchievementManager
from app.models import BaseEntity


class Achievement(BaseEntity):
    class Meta:
        ordering = ['id']
        db_table = 'achievement_achievement'

    name = models.CharField(max_length=255, null=False, unique=True)
    description = models.TextField(default='', blank=True, null=True)
    users = models.ManyToManyField('user.User', through='UserAchievement')
    threshold = models.IntegerField(blank=True, null=True)
    objects = AchievementManager()

    def __str__(self):
        return f"{self.name} : {self.description}" if self.name else self.description


class UserAchievement(models.Model):
    class Meta:
        db_table = 'achievement_userachievement'

    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)
    objects = UserAchievementManager()

    def is_owner(self, user_id):
        return self.user.id == user_id


class ActiveUserAchievement(models.Model):
    class Meta:
        db_table = 'achievement_activeuserachievement'

    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    goal_points = models.IntegerField(blank=True, null=True)
    current_points = models.IntegerField(blank=True, null=True)
    date_started = models.DateTimeField(auto_now_add=True)
    date_earned = models.DateTimeField(blank=True, null=True)
    objects = ActiveUserAchievementManager()