from rest_framework import serializers
from api.badge.models import Badge, UserBadge
from api.user.models import User


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ('id', 'name', 'description', 'threshold')

    def create(self, validated_data):
        badge = Badge.objects.create_badge(**validated_data)
        return badge

    def update(self, instance, validated_data):
        instance = Badge.objects.update_badge(instance, **validated_data)
        return instance


class UserBadgeSerializer(serializers.Serializer):
    badge_id = serializers.IntegerField()
    date_earned = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        user_id = user.id
        validated_data['user_id'] = user_id
        Badge.objects.validate_data(validated_data['badge_id'])
        UserBadge.objects.validate_data(user_id, validated_data['badge_id'])
        user_badge = UserBadge.objects.create_user_badge(**validated_data)
        return user_badge


class BadgeEarnedSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    threshold = serializers.IntegerField()
    date_earned = serializers.DateTimeField()
