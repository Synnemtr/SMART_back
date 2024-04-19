from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from app.views import (
    ListView,
    RetrieveView,
    CreateView,
    UpdateView,
    DestroyView,
)
from api.motivation.models import Motivation
from api.motivation.serializers import MotivationSerializer
from rest_framework import status
from django.db import transaction
from app.permissions import UserCanOnlyRead
from rest_framework.permissions import IsAdminUser


class MotivationDetail(RetrieveView, UpdateView, DestroyView):
    queryset = Motivation.objects.all()
    serializer_class = MotivationSerializer
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get(self, request, *args, **kwargs):
        serializer = MotivationSerializer(request.motivation)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = MotivationSerializer(request.motivation, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        Motivation.objects.delete_motivation(request.motivation)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class MotivationList(ListView, CreateView):
    serializer_class = MotivationSerializer
    search_fields = ('name')
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get_queryset(self):
        serializer = MotivationSerializer(Motivation.objects.all(), many=True)
        return serializer.data

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = MotivationSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
