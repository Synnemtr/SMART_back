from django.db import models
from api.recommender_rating.managers import RecommenderRatingManager

RATING_CHOICES = (
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

class Rating(models.Model):
    class Meta:
        unique_together = ('user', 'game_element')  
        db_table = "recommender_rating"

    user = models.ForeignKey('user.Profile', on_delete=models.CASCADE)
    game_element = models.ForeignKey('game_element.GameElement', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)
    objects = RecommenderRatingManager()

    def __str__(self):
        return f"{self.user} rated {self.game_element} with {self.rating}"