from django.db import models
from app.models import BaseEntity
from api.badge.managers import BadgeManager, UserBadgeManager


class Badge(BaseEntity):
    class Meta:
        ordering = ('id',)
        db_table = 'badge_badge'

    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    description = models.CharField(max_length=255)
    threshold = models.IntegerField(null=True, blank=True)
    objects = BadgeManager()


class UserBadge(models.Model):
    class Meta:
        unique_together = ('user', 'badge')
        db_table = 'badge_userbadge'

    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    badge = models.ForeignKey('badge.Badge', on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)
    objects = UserBadgeManager()

    def __str__(self):
        return "{} - {}".format(self.user.username, self.badge.name)

    def is_owner(self, user_id):
        return self.user.id == user_id
