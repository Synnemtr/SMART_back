from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from app.views import (
    ListView,
    RetrieveView,
    CreateView,
    UpdateView,
    DestroyView,
)
from api.user.models import User, Profile
from api.user.serializers import UserSerializer, ProfileSerializer, UserSerializerForAdmin
from rest_framework import status
from django.db import transaction
from app.permissions import IsOwner, UserDetailPermission


class UserDetail(RetrieveView, UpdateView, DestroyView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserDetailPermission]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = UserSerializer(request.user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        User.objects.delete_user(request.user)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class GetUserList(ListView):
    serializer_class = UserSerializerForAdmin
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return User.objects.all()


class CreateUserList(CreateView):
    serializer_class = UserSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetail(RetrieveView, UpdateView, DestroyView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwner | IsAdminUser]

    def get(self, request, *args, **kwargs):
        serializer = ProfileSerializer(request.user.profile)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(request.user.profile, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        Profile.objects.delete_profile(request.user.profile)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class ProfileList(CreateView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
