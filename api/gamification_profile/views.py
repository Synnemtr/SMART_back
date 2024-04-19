from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from app.views import (
    ListView,
    RetrieveView,
    CreateView,
    UpdateView,
    DestroyView,
)
from api.gamification_profile.models import GamificationProfile
from api.gamification_profile.serializers import GamificationAnswerSerializer, GamificationProfileSerializer
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class GamificationAnswerView(CreateView):
    serializer_class = GamificationAnswerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = GamificationAnswerSerializer(data=data, context={'request': request})
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GamificationProfileListView(ListView):
    serializer_class = GamificationProfileSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        profile_id = self.request.query_params.get('profile_id', None)
        # result = GamificationProfile.objects.get_answer_by_profile_id(profile_id)
        result = GamificationProfile.objects.get_all_answers()
        return result
