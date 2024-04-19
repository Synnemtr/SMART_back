from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from app.views import (
    ListView,
    RetrieveView,
    CreateView,
    UpdateView,
    DestroyView,
)
from api.badge.serializers import BadgeSerializer, UserBadgeSerializer, BadgeEarnedSerializer
from api.badge.models import Badge, UserBadge
from rest_framework import status
from app.permissions import UserCanOnlyRead, IsOwner
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class BadgeListView(ListView, CreateView):
    serializer_class = BadgeSerializer
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get_queryset(self):
        return Badge.objects.all()

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = BadgeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BadgeDetailView(RetrieveView, UpdateView, DestroyView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get(self, request, *args, **kwargs):
        serializer = BadgeSerializer(request.badge)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = BadgeSerializer(request.badge, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, *args, **kwargs):
        Badge.objects.delete_badge(request.badge)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class UserBadgeListView(CreateView):
    serializer_class = UserBadgeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = UserBadgeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserBadgeDetailView(DestroyView):
    queryset = UserBadge.objects.all()
    serializer_class = UserBadgeSerializer
    permission_classes = [IsOwner]

    def delete(self, request, *args, **kwargs):
        UserBadge.objects.delete_user_badge(request.user_badge)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class BadgeEarnedListView(ListView):
    serializer_class = BadgeEarnedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserBadge.objects.get_badges_by_user(user)
