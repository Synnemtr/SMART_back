from rest_framework import serializers
from api.game_element.models import GameElement


class GameElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameElement
        fields = ['id', 'name', 'HEXAD_12', 'description', 'user_impact', 'SDI_impact']
        read_only_fields = ('id',)

    def create(self, validated_data):
        return GameElement.objects.create_game_element(**validated_data)

    def update(self, instance, validated_data):
        GameElement.objects.validate_data(instance.id)
        instance = GameElement.objects.update_game_element(instance, **validated_data)
        return instance