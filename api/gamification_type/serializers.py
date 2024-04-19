from rest_framework import serializers
from api.gamification_type.models import GamificationType


class GamificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamificationType
        fields = ['id', 'name', 'description']
        read_only_fields = ('id',)

    def create(self, validated_data):
        return GamificationType.objects.create_gamification_type(**validated_data)

    def update(self, instance, validated_data):
        GamificationType.objects.validate_data(instance.id)
        instance = GamificationType.objects.update_type(instance, **validated_data)
        return instance
