from django.db import models
from rest_framework import exceptions
import datetime


class AchievementManager(models.Manager):
    def validate_data(self, achievement_id):
        if not self.filter(id=achievement_id).exists():
            raise exceptions.ValidationError("Achievement with id {} does not exist".format(achievement_id))

    def get_achievement(self, name):
        achievement = self.filter(name=name).first()
        return achievement

    def get_achievements_by_user_id(self, user_id):
        achievements = self.filter(users__in=[user_id]).order_by('id')
        return achievements

    def create_achievement(self, **data):
        try:
            name = data.pop('name')
        except KeyError:
            raise exceptions.ValidationError("Name is required")
        if self.filter(name=name).exists():
            raise exceptions.ValidationError("Achievement with name {} already exists".format(name))
        achievement = self.create(name=name, **data)
        list_users = data.get('users', [])
        for user in list_users:
            user_achievement = user.models.UserAchievement.objects.create(user=user, achievement=achievement)
            user_achievement.save()
        return achievement

    def update_achievement(self, achievement, **data):
        achievement.name = data.get('name', achievement.name)
        achievement.description = data.get('description', achievement.description)
        achievement.threshold = data.get('threshold', achievement.threshold)
        achievement.updated_at = datetime.datetime.now()
        achievement.save()
        return achievement

    def delete_achievement(self, achievement):
        achievement.delete()
        return achievement

    def add_user_to_achievement(self, achievement, user):
        achievement.users.add(user)
        return achievement

    def remove_user_from_achievement(self, achievement, user):
        achievement.users.remove(user)
        return achievement


class UserAchievementManager(models.Manager):
    def create_user_achievement(self, **data):
        try:
            user_id = data.pop('user_id')
            achievement_id = data.pop('achievement_id')
        except KeyError:
            raise exceptions.ValidationError("User id and achievement id are required")
        if self.filter(user_id=user_id, achievement_id=achievement_id).exists():
            raise exceptions.ValidationError("User with id {} already has achievement with id {}".format(user_id, achievement_id))
        user_achievement = self.create(user_id=user_id, achievement_id=achievement_id)
        user_achievement.save()
        return user_achievement

    def update_user_achievement(self, user_achievement, **data):
        user_achievement.user_id = data.get('user_id', user_achievement.user_id)
        user_achievement.achievement_id = data.get('achievement_id', user_achievement.achievement_id)
        user_achievement.threshold = data.get('threshold', user_achievement.threshold)
        user_achievement.save()
        return user_achievement

    def delete_user_achievement(self, user_achievement):
        user_achievement.delete()
        return user_achievement

    def validate_data(self, user_id, achievement_id):
        if self.filter(user_id=user_id, achievement_id=achievement_id).exists():
            raise exceptions.ValidationError("User with id {} already has achievement with id {}".format(user_id, achievement_id))

    def count_achievements_group_by_user(self):
        return self.values('user_id').annotate(total=models.Count('user_id')).order_by('-total')

    def get_users_by_achievement_id_order_by_date(self, achievement_id):
        result = self.filter(achievement_id=achievement_id).order_by('date_earned')
        return result


class ActiveUserAchievementManager(models.Manager):
    def create_active_user_achievement(self, **data):
        try:
            user_id = data.pop('user_id')
            achievement_id = data.pop('achievement_id')
        except KeyError:
            raise exceptions.ValidationError("User id and achievement id are required")
        if self.filter(user_id=user_id, achievement_id=achievement_id).exists():
            raise exceptions.ValidationError("User with id {} already has active achievement with id {}".format(user_id, achievement_id))
        active_user_achievement = self.create(user_id=user_id, achievement_id=achievement_id, **data)
        active_user_achievement.save()
        return active_user_achievement

    def update_active_user_achievement(self, active_user_achievement, **data):
        active_user_achievement.user_id = data.get('user_id', active_user_achievement.user_id)
        active_user_achievement.achievement_id = data.get('achievement_id', active_user_achievement.achievement_id)
        active_user_achievement.current_points = data.get('current_points', active_user_achievement.current_points)
        active_user_achievement.save()
        return active_user_achievement

    def delete_active_user_achievement(self, active_user_achievement):
        active_user_achievement.delete()
        return active_user_achievement

    def validate_data(self, user_id, achievement_id):
        if self.filter(user_id=user_id, achievement_id=achievement_id).exists():
            raise exceptions.ValidationError("User with id {} already has active achievement with id {}".format(user_id, achievement_id))