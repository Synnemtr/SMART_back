from django.urls import path
from api.motivation.views import (
    MotivationList,
    MotivationDetail,
)

urlpatterns = [
    path("", MotivationList.as_view({'get': 'list', 'post': 'create'})),
    path("<int:pk>/", MotivationDetail.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
