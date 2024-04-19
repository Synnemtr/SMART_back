from django.urls import path
from api.motivation_profile.views import (
    MotivationAnswerView,
    MotivationProfileListView,
)

urlpatterns = [
    path("questions/", MotivationAnswerView.as_view({'post': 'create'})),
    path("profiles/", MotivationProfileListView.as_view({'get': 'list'})),
]
