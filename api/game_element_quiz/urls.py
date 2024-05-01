from django.urls import path
from api.game_element_quiz.views import (
    GameQuizList,
    GameQuizDetail,
)

urlpatterns = [
    path("", GameQuizList.as_view({'get': 'list', 'post': 'create'})),
    path("<int:pk>/", GameQuizDetail.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]