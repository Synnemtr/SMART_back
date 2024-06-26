from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from app.views import (
    ListView,
    RetrieveView,
    CreateView,
    UpdateView,
    DestroyView,
)
from api.gamification_type.models import GamificationType
from api.gamification_type.serializers import GamificationTypeSerializer
from rest_framework import status
from django.db import transaction
from app.permissions import UserCanOnlyRead
from rest_framework.permissions import IsAdminUser


class GamificationTypeDetail(RetrieveView, UpdateView, DestroyView):
    queryset = GamificationType.objects.all()
    serializer_class = GamificationTypeSerializer
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get(self, request, *args, **kwargs):
        serializer = GamificationTypeSerializer(request.type)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = GamificationTypeSerializer(request.type, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        GamificationType.objects.delete_type(request.type)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class GamificationTypeList(ListView, CreateView):
    serializer_class = GamificationTypeSerializer
    search_fields = ('name', 'description')
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get_queryset(self):
        serializer = GamificationTypeSerializer(GamificationType.objects.all(), many=True)
        return serializer.data

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = GamificationTypeSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    