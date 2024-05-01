from django.urls import path
from api.game_element.views import (
    GamificationElementList,
    GamificationElementDetail
)

urlpatterns = [
    path("", GamificationElementList.as_view({'get': 'list', 'post': 'create'})),
    path("<int:pk>/", GamificationElementDetail.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]