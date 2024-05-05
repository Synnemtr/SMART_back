from django.db import models
from api.recommender_system.managers import RecommenderSystemManger
from api.game_element.models import GameElement


class RecommenderSystem(models.Model):
    class Meta:
        db_table = "recommender_system"

    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    game_element = models.ForeignKey('game_element.GameElement', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = RecommenderSystemManger()

    def __str__(self):
        return f'Recommendation for {self.user.username}: {self.game_element.name}'
    