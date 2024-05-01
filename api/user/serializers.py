from api.user.models import User, Profile
from rest_framework import serializers
from datetime import date
from api.gamification_profile.models import GamificationProfile
from api.motivation_profile.models import MotivationProfile


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
        # read_only_fields = ("user", "picture")
        read_only_fields = ("user",)
    # Custom read-only field for BMR
    bmr = serializers.SerializerMethodField()

    # Custom read-only field for BMI
    bmi = serializers.SerializerMethodField()

    # Custom read-only field for HEXAD-12 type
    HEXAD_12_type = serializers.SerializerMethodField()
    HEXAD_12_scores = serializers.SerializerMethodField()

    # Custom read-only field for motivation
    motivation_SDI = serializers.SerializerMethodField()
    motivation_scores = serializers.SerializerMethodField()

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
    
    def get_HEXAD_12_type(self, obj):
        gamification_profiles = GamificationProfile.objects.filter(profile=obj).select_related('gamification_type').order_by('-score')
        if gamification_profiles:
            return gamification_profiles[0].gamification_type.name
        return None
    
    def get_HEXAD_12_scores(self, obj):
        gamification_profiles = GamificationProfile.objects.filter(profile=obj).select_related('gamification_type').order_by('-score')
        if gamification_profiles:
            return {gp.gamification_type.name: gp.score for gp in gamification_profiles}
        return []
    
    def get_motivation_SDI(self, obj):
        motivation_profiles = MotivationProfile.objects.filter(profile=obj).select_related('motivation')

        intrinsic_score = self.get_average_score(motivation_profiles, 'Intrinsic motivation')
        integrated_score = self.get_average_score(motivation_profiles, 'Integrated regulation')
        identified_score = self.get_average_score(motivation_profiles, 'Identified regulation')
        introjected_score = self.get_average_score(motivation_profiles, 'Introjected regulation')
        extrinsic_score = self.get_average_score(motivation_profiles, 'External regulation')
        amotivation_score = self.get_average_score(motivation_profiles, 'Amotivation')

        motivation_score = 3*intrinsic_score + 2*integrated_score + identified_score - introjected_score - 2*extrinsic_score - 3*amotivation_score

        return motivation_score

    def get_average_score(self, profiles, motivation_name):
        scores = [profile.score for profile in profiles if profile.motivation.name == motivation_name]
        return sum(scores) / len(scores) if scores else 0
        
    def get_motivation_scores(self, obj):
        motivation_profiles = MotivationProfile.objects.filter(profile=obj).select_related('motivation').order_by('motivation_id')
        if motivation_profiles:
            return {mp.motivation.name: mp.score for mp in motivation_profiles}
        return []

    # picture = serializers.ImageField(use_url=True, required=False)

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
