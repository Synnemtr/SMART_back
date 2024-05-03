from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from app.views import (
    ListView,
    RetrieveView,
    CreateView,
    UpdateView,
    DestroyView,
)
from api.recommender_rating.models import Rating
from api.recommender_rating.serializers import RecommenderRatingSerializer
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class RatingList(ListView, CreateView):
    serializer_class = RecommenderRatingSerializer
    permission_classes = [IsAuthenticated | IsAdminUser]

    def get_queryset(self):
        serializer = RecommenderRatingSerializer(Rating.objects.all(), many=True)
        return serializer.data

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = RecommenderRatingSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

