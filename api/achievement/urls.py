from django.urls import path
from api.achievement.views import (
    AchievementList,
    AchievementDetail,
    AchievementsForUserView,
    UserAchievementList,
    UserAchievementDetail,
    RankingAchievementView,
    RankingDateEarnedAchievementView,
    ActiveUserAchievementForUserView, 
    ActiveUserAchievementDetail, 
    ActiveUserAchievementList,
)

urlpatterns = [
    path("", AchievementList.as_view({'get': 'list', 'post': 'create'})),
    path("<int:pk>/", AchievementDetail.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path("user/", AchievementsForUserView.as_view({'get': 'list'})),
    path("list/user/", UserAchievementList.as_view({'post': 'create'})),
    path("list/user/<int:pk>/", UserAchievementDetail.as_view({'delete': 'destroy'})),
    path("ranking/", RankingAchievementView.as_view({'get': 'list'})),
    # path("ranking/date/<int:pk>/", RankingDateEarnedAchievementView.as_view({'get': 'list'})),
    path("active/", ActiveUserAchievementForUserView.as_view({'get': 'list'})),
    path("active/user/", ActiveUserAchievementList.as_view({'post': 'create'})),
    path("active/user/<int:pk>/", ActiveUserAchievementDetail.as_view({'delete': 'destroy'})),
]
