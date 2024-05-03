from django.urls import path
from api.macronutrient.views import (
    MacronutrientList,
    MacronutrientDetail
)

urlpatterns = [
    path("", MacronutrientList.as_view({'get': 'list', 'post': 'create'})),
    path("<int:pk>/", MacronutrientDetail.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
