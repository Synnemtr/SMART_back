from rest_framework import serializers
from api.recommender_rating.models import Rating
from api.user.models import User
from api.game_element.models import GameElement


class RecommenderRatingSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    game_element_id = serializers.IntegerField()
    rating = serializers.IntegerField()

    class Meta:
        model = Rating
        fields = ['user_id', 'game_element_id', 'rating']
    
    def validate(self, data):
        user_id = data.get("user_id")
        game_element_id = data.get("game_element_id")
        rating = data.get("rating")

        if not User.objects.filter(id=user_id).exists():
            raise serializers.ValidationError("User with given ID does not exist.")

        if not GameElement.objects.filter(id=game_element_id).exists():
            raise serializers.ValidationError("Game element with given ID does not exist.")

        if rating < 0 or rating > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5.")

        return data

    def create(self, validated_data):
        new_rating = Rating.objects.create_rating(**validated_data)
        return new_rating
