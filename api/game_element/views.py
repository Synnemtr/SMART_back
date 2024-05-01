from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from app.views import (
    ListView,
    RetrieveView,
    CreateView,
    UpdateView,
    DestroyView,
)
from api.game_element.models import GameElement
from api.game_element.serializers import GameElementSerializer
from rest_framework import status
from django.db import transaction
from app.permissions import UserCanOnlyRead
from rest_framework.permissions import IsAdminUser


class GamificationElementDetail(RetrieveView, UpdateView, DestroyView):
    queryset = GameElement.objects.all()
    serializer_class = GameElementSerializer
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get(self, request, *args, **kwargs):
        serializer = GameElementSerializer(request.elements)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = GameElementSerializer(request.element, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        GameElement.objects.delete_game_element(request.type)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class GamificationElementList(ListView, CreateView):
    serializer_class = GameElementSerializer
    search_fields = ('name', 'HEXAD_12')
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get_queryset(self):
        serializer = GameElementSerializer(GameElement.objects.all(), many=True)
        return serializer.data

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = GameElementSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    