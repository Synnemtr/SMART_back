from rest_framework import serializers
from api.macronutrient.models import Macronutrient


class MacronutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Macronutrient
        fields = ["id", "name", "calories_per_gram"]
        read_only_fields = ("id",)

    def create(self, validated_data):
        macronutrient = Macronutrient.objects.create_macronutrient(**validated_data)
        return macronutrient

    def update(self, instance, validated_data):
        instance = Macronutrient.objects.update_macronutrient(instance, **validated_data)
        return instance
