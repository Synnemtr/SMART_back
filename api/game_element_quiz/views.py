from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from app.views import (
    ListView,
    RetrieveView,
    CreateView,
    UpdateView,
    DestroyView,
)
from api.game_element_quiz.models import GameQuiz
from api.game_element_quiz.serializers import GameQuizSerializer
from rest_framework import status
from django.db import transaction
from app.permissions import UserCanOnlyRead
from rest_framework.permissions import IsAdminUser


class GameQuizDetail(RetrieveView, UpdateView, DestroyView):
    queryset = GameQuiz.objects.all()
    serializer_class = GameQuizSerializer
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get(self, request, *args, **kwargs):
        serializer = GameQuizSerializer(self.get_object())
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = GameQuizSerializer(self.get_object(), data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        GameQuiz.objects.delete_game_quiz(self.get_object())
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class GameQuizList(ListView, CreateView):
    serializer_class = GameQuizSerializer
    search_fields = ('question', 'option_one', 'option_two', 'option_three', 'option_four', 'correct_answer')
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get_queryset(self):
        return GameQuiz.objects.all()

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = GameQuizSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)