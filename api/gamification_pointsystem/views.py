from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from app.views import (
    ListView,
    RetrieveView,
    CreateView,
    UpdateView,
    DestroyView,
)
from api.gamification_pointsystem.models import GamificationPointsystem
from api.gamification_pointsystem.serializers import GamificationPointsystemSerializer
from rest_framework import status
from django.db import transaction
from app.permissions import UserCanOnlyRead
from rest_framework.permissions import IsAdminUser


class GamificationPointsystemDetail(RetrieveView, UpdateView, DestroyView):
    queryset = GamificationPointsystem.objects.all()
    serializer_class = GamificationPointsystemSerializer
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get(self, request, *args, **kwargs):
        serializer = GamificationPointsystemSerializer(request.pointsystem)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = GamificationPointsystemSerializer(request.pointsystem, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        GamificationPointsystem.objects.delete_pointsystem(request.pointsystem)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class GamificationPointsystemList(ListView, CreateView):
    serializer_class = GamificationPointsystemSerializer
    search_fields = ('element_name', 'description')
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get_queryset(self):
        serializer = GamificationPointsystemSerializer(GamificationPointsystem.objects.all(), many=True)
        return serializer.data

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = GamificationPointsystemSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)