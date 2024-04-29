from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from app.views import (
    ListView,
    RetrieveView,
    CreateView,
    UpdateView,
    DestroyView,
)
from api.gamification_element.models import GamificationElement
from api.gamification_element.serializers import GamificationElementSerializer
from rest_framework import status
from django.db import transaction
from app.permissions import UserCanOnlyRead
from rest_framework.permissions import IsAdminUser


class GamificationElementDetail(RetrieveView, UpdateView, DestroyView):
    queryset = GamificationElement.objects.all()
    serializer_class = GamificationElementSerializer
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get(self, request, *args, **kwargs):
        serializer = GamificationElementSerializer(request.elements)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = GamificationElementSerializer(request.element, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        GamificationElement.objects.delete_gamification_type(request.type)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class GamificationElementList(ListView, CreateView):
    serializer_class = GamificationElementSerializer
    search_fields = ('name', 'HEXAD_12')
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get_queryset(self):
        serializer = GamificationElementSerializer(GamificationElement.objects.all(), many=True)
        return serializer.data

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = GamificationElementSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    