from rest_framework import serializers
from api.gamification_pointsystem.models import GamificationPointsystem


class GamificationPointsystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamificationPointsystem
        fields = ['id', 'element_name', 'description', 'point']
        read_only_fields = ('id',)

    def create(self, validated_data):
        return GamificationPointsystem.objects.create_gamification_pointsystem(**validated_data)

    def update(self, instance, validated_data):
        GamificationPointsystem.objects.validate_data(instance.element_name)
        instance = GamificationPointsystem.objects.update_gamification_pointsystem(instance, **validated_data)
        return instance