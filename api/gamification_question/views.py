from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from app.views import (
    ListView,
    RetrieveView,
    CreateView,
    UpdateView,
    DestroyView,
)
from api.gamification_question.models import GamificationQuestion
from api.gamification_question.serializers import GamificationQuestionSerializer
from rest_framework import status
from django.db import transaction
from app.permissions import UserCanOnlyRead
from rest_framework.permissions import IsAdminUser


class GamificationQuestionDetail(RetrieveView, UpdateView, DestroyView):
    queryset = GamificationQuestion.objects.all()
    serializer_class = GamificationQuestionSerializer
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get(self, request, *args, **kwargs):
        serializer = GamificationQuestionSerializer(request.question)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = GamificationQuestionSerializer(request.question, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        GamificationQuestion.objects.delete_gamification_question(request.question)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class GamificationQuestionList(ListView, CreateView):
    serializer_class = GamificationQuestionSerializer
    search_fields = ('question', 'gamification_type')
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get_queryset(self):
        serializer = GamificationQuestionSerializer(GamificationQuestion.objects.all(), many=True)
        return serializer.data

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = GamificationQuestionSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
