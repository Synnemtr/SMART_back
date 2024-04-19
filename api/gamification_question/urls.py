from django.urls import path
from api.gamification_question.views import (
    GamificationQuestionList,
    GamificationQuestionDetail,
)

urlpatterns = [
    path("", GamificationQuestionList.as_view({'get': 'list', 'post': 'create'})),
    path("<int:pk>/", GamificationQuestionDetail.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
