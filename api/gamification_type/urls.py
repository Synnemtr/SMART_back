from django.urls import path
from api.gamification_type.views import (
    GamificationTypeList,
    GamificationTypeDetail
)

urlpatterns = [
    path("", GamificationTypeList.as_view({'get': 'list', 'post': 'create'})),
    path("<int:pk>/", GamificationTypeDetail.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]