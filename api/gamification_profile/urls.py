from django.urls import path
from api.gamification_profile.views import (
    GamificationAnswerView,
    GamificationProfileListView,
)

urlpatterns = [
    path("questions/", GamificationAnswerView.as_view({'post': 'create'})),
    path("profiles/", GamificationProfileListView.as_view({'get': 'list'})),
]
