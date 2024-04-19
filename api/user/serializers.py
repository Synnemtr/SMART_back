from api.user.models import User, Profile
from rest_framework import serializers
from datetime import date


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password",
                  "email", "phone_number",
                  "first_name", "last_name", "full_name",
                  "is_superuser", "date_joined", "last_login"
                  ]

    def create(self, validated_data):
        User.objects.validate_superuser(self.context['request'].user, **validated_data)
        is_superuser = validated_data.pop('is_superuser', None)
        user = User.objects.create_user(is_superuser, **validated_data)
        return user

    def update(self, instance, validated_data):
        User.objects.validate_superuser(self.context['request'].user, **validated_data)
        instance = User.objects.update_user(instance, **validated_data)
        return instance


class UserSerializerForAdmin(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username",
                  "is_superuser", "date_joined", "last_login"
                  ]


class UserAchievementRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username",
                  "email", "phone_number",
                  "first_name", "last_name", "full_name",
                  "achievement_count"
                  ]

    achievement_count = serializers.IntegerField(read_only=True)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ("user", "picture")
    # Custom read-only field for BMR
    bmr = serializers.SerializerMethodField()

    # Custom read-only field for BMI
    bmi = serializers.SerializerMethodField()

    def get_bmi(self,obj):
        if obj.height and obj.weight:
            bmi = round(obj.weight / ((obj.height / 100) ** 2), 2)
        else:
            bmi = None
        return bmi    
    

    def get_bmr(self,obj):
        if obj.weight and obj.height and obj.date_of_birth:
            today = date.today()
            age = today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))

            if obj.sex == 'MAN':
                bmr = round((10 * obj.weight) + (6.25 * obj.height) - (5 * age) + 5, 2)
            else:
                bmr = round((10 * obj.weight) + (6.25 * obj.height) - (5 * age) - 161, 2)
        else: bmr=None
        return bmr

    picture = serializers.ImageField(use_url=True, required=False)

    def create(self, validated_data):
        user = self.context['request'].user
        profile = Profile.objects.create_profile(user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        instance = Profile.objects.update_profile(instance, **validated_data)
        return instance


class UserAchievementDateRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username",
                  "email", "phone_number",
                  "first_name", "last_name", "full_name",
                  "date_earned"
                  ]

    date_earned = serializers.DateTimeField(read_only=True)
