from rest_framework import serializers
from api.motivation.models import Motivation


class MotivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motivation
        fields = ['id', 'name']
        read_only_fields = ('id',)

    def create(self, validated_data):
        return Motivation.objects.create_motivation(**validated_data)

    def update(self, instance, validated_data):
        instance = Motivation.objects.update_motivation(instance, **validated_data)
        return instance