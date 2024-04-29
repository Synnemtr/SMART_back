from rest_framework import serializers
from api.achievement.models import Achievement, UserAchievement, ActiveUserAchievement
from api.user.models import User


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('id', 'name', 'description', 'threshold')

    def create(self, validated_data):
        achievement = Achievement.objects.create_achievement(**validated_data)
        return achievement

    def update(self, instance, validated_data):
        instance = Achievement.objects.update_achievement(instance, **validated_data)
        return instance


class UserAchievementSerializer(serializers.Serializer):
    achievement_id = serializers.IntegerField()
    date_earned = serializers.DateTimeField(read_only=True)

    def validate(self, data):
        user_id = self.context['request'].user.id
        achievement_id = data.get('achievement_id')
        UserAchievement.objects.validate_data(user_id, achievement_id)
        User.objects.validate_data(user_id)
        Achievement.objects.validate_data(achievement_id)
        return data

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        user_achievement = UserAchievement.objects.create_user_achievement(**validated_data)
        Achievement.objects.add_user_to_achievement(user_achievement.achievement, user_achievement.user)
        return user_achievement

    def update(self, instance, validated_data):
        instance = UserAchievement.objects.update_user_achievement(instance, **validated_data)
        return instance


class ActiveUserAchievementSerializer(serializers.Serializer):
    achievement_id = serializers.IntegerField()
    current_points = serializers.IntegerField(required=False)
    date_started = serializers.DateTimeField(read_only=True)

    def validate(self, data):
        user_id = self.context['request'].user.id
        achievement_id = data.get('achievement_id')
        ActiveUserAchievement.objects.validate_data(user_id, achievement_id)
        User.objects.validate_data(user_id)
        Achievement.objects.validate_data(achievement_id)
        return data

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        active_user_achievement = ActiveUserAchievement.objects.create_active_user_achievement(**validated_data)
        return active_user_achievement

    def update(self, instance, validated_data):
        instance = ActiveUserAchievement.objects.update_active_user_achievement(instance, **validated_data)
        return instance
    