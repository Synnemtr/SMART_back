from app.views import (
    ListView,
    RetrieveView,
    CreateView,
    UpdateView,
    DestroyView,
)
from api.achievement.models import Achievement, UserAchievement, ActiveUserAchievement
from api.user.models import User
from api.achievement.serializers import AchievementSerializer, UserAchievementSerializer, ActiveUserAchievementSerializer
from api.user.serializers import UserAchievementRankingSerializer, UserAchievementDateRankingSerializer
from rest_framework import status
from django.db import transaction
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import JsonResponse, HttpResponse
from app.permissions import UserCanOnlyRead, IsOwner


class AchievementList(ListView, CreateView):
    serializer_class = AchievementSerializer
    search_fields = ('name', 'description')
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get_queryset(self):
        serializer = AchievementSerializer(Achievement.objects.all(), many=True)
        return serializer.data

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = AchievementSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AchievementDetail(RetrieveView, UpdateView, DestroyView):
    serializer_class = AchievementSerializer
    permission_classes = [UserCanOnlyRead | IsAdminUser]
    queryset = Achievement.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = AchievementSerializer(request.achievement)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = AchievementSerializer(request.achievement, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        Achievement.objects.delete_achievement(request.achievement)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class UserAchievementList(CreateView):
    model = UserAchievement
    serializer_class = UserAchievementSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserAchievement.objects.all()

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = UserAchievementSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAchievementDetail(DestroyView):
    model = UserAchievement
    serializer_class = UserAchievementSerializer
    permission_classes = [IsOwner]
    queryset = UserAchievement.objects.all()

    def delete(self, request, *args, **kwargs):
        user_achievement = request.user_achievement
        Achievement.objects.remove_user_from_achievement(user_achievement.achievement,
                                                         user_achievement.user)
        UserAchievement.objects.delete_user_achievement(user_achievement)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class AchievementsForUserView(ListView):
    model = Achievement
    serializer_class = AchievementSerializer
    queryset = Achievement.objects.all()

    def get_queryset(self):
        result = Achievement.objects.get_achievements_by_user_id(self.request.user.id)
        serializer = AchievementSerializer(result, many=True)
        return serializer.data


class ActiveUserAchievementList(CreateView):
    model = ActiveUserAchievement
    serializer_class = ActiveUserAchievementSerializer
    permission_classes = [IsAuthenticated]
    queryset = ActiveUserAchievement.objects.all()

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = ActiveUserAchievementSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActiveUserAchievementDetail(UpdateView, DestroyView):
    model = ActiveUserAchievement
    serializer_class = ActiveUserAchievementSerializer
    permission_classes = [IsOwner]
    queryset = ActiveUserAchievement.objects.all()

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = self.serializer_class(self.get_object(), data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        active_user_achievement = self.get_object()
        ActiveUserAchievement.objects.delete_active_user_achievement(active_user_achievement)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class ActiveUserAchievementForUserView(ListView):
    serializer_class = ActiveUserAchievementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return ActiveUserAchievement.objects.filter(user_id=user_id)


class RankingAchievementView(ListView):
    serializer_class = UserAchievementRankingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryData = UserAchievement.objects.count_achievements_group_by_user()
        rankings = User.objects.get_number_achievement_user(queryData)
        serializer = UserAchievementRankingSerializer(rankings, many=True)
        return serializer.data


class RankingDateEarnedAchievementView(ListView):
    model = Achievement
    serializer_class = UserAchievementDateRankingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        id_achievement = self.kwargs['pk']
        queryData = UserAchievement.objects.get_users_by_achievement_id_order_by_date(id_achievement)
        rankings = User.objects.get_users_date_earned_by_achievement(queryData)
        serializer = UserAchievementDateRankingSerializer(rankings, many=True)
        return serializer.data
