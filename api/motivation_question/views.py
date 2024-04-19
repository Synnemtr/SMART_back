from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from app.views import (
    ListView,
    RetrieveView,
    CreateView,
    UpdateView,
    DestroyView,
)
from api.motivation_question.models import MotivationQuestion
from api.motivation_question.serializers import MotivationQuestionSerializer
from rest_framework import status
from django.db import transaction
from app.permissions import UserCanOnlyRead
from rest_framework.permissions import IsAdminUser


class MotivationQuestionDetail(RetrieveView, UpdateView, DestroyView):
    queryset = MotivationQuestion.objects.all()
    serializer_class = MotivationQuestionSerializer
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get(self, request, *args, **kwargs):
        serializer = MotivationQuestionSerializer(request.question)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = MotivationQuestionSerializer(request.question, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        MotivationQuestion.objects.delete_motivation_question(request.question)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class MotivationQuestionList(ListView, CreateView):
    serializer_class = MotivationQuestionSerializer
    search_fields = ('question', 'motivation')
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get_queryset(self):
        serializer = MotivationQuestionSerializer(MotivationQuestion.objects.all(), many=True)
        return serializer.data

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = MotivationQuestionSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
