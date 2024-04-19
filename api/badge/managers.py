from django.db import models, connection
from rest_framework import exceptions
import datetime


class BadgeManager(models.Manager):
    def validate_data(self, badge_id):
        if not self.filter(id=badge_id).exists():
            raise exceptions.ValidationError("Badge with id {} does not exist".format(badge_id))

    def get_badges(self):
        badges = self.all()
        return badges

    def get_badge_by_id(self, badge_id):
        if not self.filter(id=badge_id).exists():
            raise exceptions.ValidationError("Badge with id {} does not exist".format(badge_id))
        badge = self.get(id=badge_id)
        return badge

    def create_badge(self, **data):
        try:
            name = data.pop('name')
        except KeyError:
            raise exceptions.ValidationError("Name is required")
        badge = self.create(name=name, **data)
        return badge

    def update_badge(self, badge, **data):
        badge.name = data.get('name', badge.name)
        badge.description = data.get('description', badge.description)
        badge.threshold = data.get('threshold', badge.threshold)
        badge.updated_at = datetime.datetime.now()
        badge.save()
        return badge

    def delete_badge(self, badge):
        badge.delete()
        return badge


class UserBadgeManager(models.Manager):
    def validate_data(self, user_id, badge_id):
        if self.filter(user_id=user_id, badge_id=badge_id).exists():
            raise exceptions.ValidationError("User {} already has badge {}".format(user_id, badge_id))

    def create_user_badge(self, **data):
        try:
            user_id = data.pop('user_id')
            badge_id = data.pop('badge_id')
        except KeyError:
            raise exceptions.ValidationError("User id and badge id are required")
        user_badge = self.create(user_id=user_id, badge_id=badge_id)
        user_badge.save()
        return user_badge

    def delete_user_badge(self, user_badge):
        user_badge.delete()
        return user_badge

    def get_badges_by_user(self, user):
        query = """
        SELECT badge_badge.name, badge_badge.description, badge_badge.threshold, badge_userbadge.date_earned
        FROM badge_badge, badge_userbadge
        WHERE badge_badge.id = badge_userbadge.badge_id AND badge_userbadge.user_id = %s
        ORDER BY badge_userbadge.date_earned DESC
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [user.id])
            badges = cursor.fetchall()
        labels = ['name', 'description', 'threshold', 'date_earned']
        result = [dict(zip(labels, badge)) for badge in badges]
        return result
