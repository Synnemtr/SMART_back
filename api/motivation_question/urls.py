from django.urls import path
from api.motivation_question.views import (
    MotivationQuestionList,
    MotivationQuestionDetail
)

urlpatterns = [
    path("", MotivationQuestionList.as_view({'get': 'list', 'post': 'create'})),
    path("<int:pk>/", MotivationQuestionDetail.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
