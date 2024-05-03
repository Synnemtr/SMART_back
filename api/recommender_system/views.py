from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from app.views import (
    ListView,
    RetrieveView,
    CreateView,
    UpdateView,
    DestroyView,
)
from api.recommender_system.models import RecommenderSystem
from api.recommender_system.serializers import RecommenderSystemSerializer
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class RecommendationView(ListView):
    serializer_class = RecommenderSystemSerializer

    def get_queryset(self):
        user = self.request.user
        recommendations = RecommenderSystem.objects.get_user_recommendations(user.id)
        return recommendations
