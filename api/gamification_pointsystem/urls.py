from django.urls import path
from api.gamification_pointsystem.views import (
    GamificationPointsystemList,
    GamificationPointsystemDetail
)

urlpatterns = [
    path("", GamificationPointsystemList.as_view({'get': 'list', 'post': 'create'})),
    path("<int:pk>/", GamificationPointsystemDetail.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]