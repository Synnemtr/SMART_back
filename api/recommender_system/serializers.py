from rest_framework import serializers
from api.recommender_system.models import RecommenderSystem
from api.game_element.serializers import GameElementSerializer


class RecommenderSystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecommenderSystem
        depth = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "GET":
            self.Meta.depth = 1
            self.Meta.exclude = None
            self.Meta.fields = '__all__'
        else:
            self.Meta.depth = 0
            self.Meta.exclude = ["user"]
            self.Meta.fields = None