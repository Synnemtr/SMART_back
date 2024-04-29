from rest_framework import serializers
from api.gamification_element.models import GamificationElement


class GamificationElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamificationElement
        fields = ['id', 'name', 'HEXAD_12', 'description', 'user_impact', 'SDI_impact']
        read_only_fields = ('id',)

    def create(self, validated_data):
        return GamificationElement.objects.create_gamification_element(**validated_data)

    def update(self, instance, validated_data):
        GamificationElement.objects.validate_data(instance.id)
        instance = GamificationElement.objects.update_gamification_element(instance, **validated_data)
        return instance