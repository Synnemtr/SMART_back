from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from rest_framework import exceptions
from django.db import models


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    def validate_superuser(self, user, **data):
        if not user.is_superuser:
            is_superuser = data.pop('is_superuser', None)
            data['is_superuser'] = is_superuser
            if is_superuser:
                raise exceptions.ValidationError("You are not allowed to create superuser")

    def validate_data(self, user_id):
        if not self.filter(id=user_id).exists():
            raise exceptions.ValidationError("User with id {} does not exist".format(user_id))

    def create_user(self, is_superuser=False, **data):
        """Create and save a regular User with the given email and password."""
        data.setdefault("is_staff", is_superuser)
        data.setdefault("is_superuser", is_superuser)
        try:
            username = data.pop('username')
        except KeyError:
            raise exceptions.ValidationError("Username is required")

        user = self.filter(username=username).first()
        if user:
            raise exceptions.ValidationError("Username is already taken")

        try:
            password = data['password']
        except KeyError:
            password = '123'
        user = self.model(username=username, **data)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, **data):
        """Create and save a SuperUser with the given email and password."""
        data.setdefault('is_superuser', True)
        data.setdefault('is_staff', True)
        try:
            username = data.pop('username')
        except KeyError:
            raise exceptions.ValidationError("Username is required")

        user = self.filter(username=username).first()
        if user:
            raise exceptions.ValidationError("Username is already taken")

        try:
            password = data['password']
        except KeyError:
            password = '123'
        user = self.model(username=username, **data)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def update_user(self, user, **data):
        user.username = data.get('username', user.username)
        user.set_password(data.get('password', user.password))
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.is_superuser = data.get('is_superuser', user.is_superuser)
        user.is_active = data.get('is_active', user.is_active)
        user.save()
        return user

    def set_last_login(self, user):
        user.last_login = timezone.now()
        user.save()

    def delete_user(self, user):
        user.delete()
        return user

    def get_number_achievement_user(self, data):
        rankings = []
        for item in data:
            user = self.get(id=item['user_id'])
            user.achievement_count = item['total']
            rankings.append(user)
        return rankings

    def get_users_date_earned_by_achievement(self, data):
        rankings = []
        for item in data:
            user = item.user
            user.date_earned = item.date_earned
            rankings.append(user)
        return rankings

    def get_user_by_username(self, username):
        return self.filter(username=username).first()


class ProfileManager(models.Manager):
    def create_profile(self, user, **data):
        profile = self.model(user=user, **data)
        profile.save()
        return profile

    def update_profile(self, profile, **data):
        # profile.picture = data.get('picture', profile.picture)
        profile.sex = data.get('sex', profile.sex)
        profile.age = data.get('age', profile.age)
        profile.date_of_birth = data.get('date_of_birth', profile.date_of_birth)
        profile.weight = data.get('weight', profile.weight)
        profile.height = data.get('height', profile.height)
        profile.body_fat = data.get('body_fat', profile.body_fat)
        profile.goal = data.get('goal', profile.goal)
        profile.sub_goal = data.get('sub_goal', profile.sub_goal)
        profile.goal_progress = data.get('goal_progress', profile.goal_progress)
        profile.total_points = data.get('total_points', profile.total_points)
        profile.training_per_week = data.get('training_per_week', profile.training_per_week)
        profile.preferred_diet = data.get('preferred_diet', profile.preferred_diet)

        profile.save()
        return profile

    def delete_profile(self, profile):
        profile.delete()
        return profile
