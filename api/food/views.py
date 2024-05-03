from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from app.views import (
    ListView,
    RetrieveView,
    CreateView,
    UpdateView,
    DestroyView,
)
from api.food.serializers import FoodSerializer, MacronutrientFoodSerializer, FoodIntakeSerializer, \
    FoodByUserSerializer, RankingFoodByCaloriesSerializer, PlannedFoodSerializer, UserFoodConsumptionSerializer
from api.food.models import Food, MacronutrientFood, FoodIntake, PlannedFood
from rest_framework import status
from django.db import transaction
from app.permissions import UserCanOnlyRead, IsOwner
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db.models import Count


class FoodTakenByUser(ListView):
    serializer_class = FoodIntakeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        #food_intakes = FoodIntake.objects.get_food_taken_by_user_on_date(user)
        food_intakes = FoodIntake.objects.filter(user=user)        
        return food_intakes


class FoodTakenByUserDate(ListView):
    serializer_class = FoodIntakeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        date = self.request.query_params.get('date', None)
        #food_intakes = FoodIntake.objects.get_food_taken_by_user_on_date(user, date)
        if date: food_intakes = FoodIntake.objects.filter(user=user).filter(date__date=date)
        else:food_intakes = FoodIntake.objects.filter(user=user)
        return food_intakes


class FoodIntakeDetail(RetrieveView, UpdateView, DestroyView):
    queryset = FoodIntake.objects.all()
    serializer_class = FoodIntakeSerializer
    permission_classes = [IsOwner]

    def get(self, request, *args, **kwargs):
        serializer = FoodIntakeSerializer(request.food_intake)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = FoodIntakeSerializer(request.food_intake, data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        request.food_intake.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class FoodIntakeList(ListView, CreateView):
    queryset = FoodIntake.objects.all()
    serializer_class = FoodIntakeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FoodIntake.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = FoodIntakeSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save(user=request.user)
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlannedFoodDetail(RetrieveView, UpdateView, DestroyView):
    queryset = PlannedFood.objects.all()
    serializer_class = PlannedFoodSerializer
    permission_classes = [IsOwner]

    def get(self, request, *args, **kwargs):
        serializer = PlannedFoodSerializer(request.planned_food)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = PlannedFoodSerializer(request.planned_food, data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        request.planned_food.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

class PlannedFoodList(ListView, CreateView):
    queryset = PlannedFood.objects.all()
    serializer_class = PlannedFoodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PlannedFood.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = PlannedFoodSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save(user=request.user)
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FoodDetail(RetrieveView, UpdateView, DestroyView):
    class Meta:
        model = Food
        fields = ('id', 'name', 'code', 'macronutrients')
        read_only_fields = ('id',)
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get(self, request, *args, **kwargs):
        serializer = FoodSerializer(request.food)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = FoodSerializer(request.food, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        Food.objects.delete_food(request.food)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class FoodList(ListView, CreateView):
    class Meta:
        model = Food
        fields = ('id', 'name', 'code')
        read_only_fields = ('id',)
    serializer_class = FoodSerializer
    permission_classes = [UserCanOnlyRead | IsAdminUser]

    def get_queryset(self):
        return Food.objects.all()

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = FoodSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RankingFoodByUsers(ListView):
    serializer_class = UserFoodConsumptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        rankings = FoodIntake.objects.values('user').annotate(total_food_consumed=Count('food')).order_by('-total_food_consumed')
        serializer = self.serializer_class(rankings, many=True)
        return serializer.data
    

class RankingFoodByCalories(ListView):
    serializer_class = RankingFoodByCaloriesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        results = MacronutrientFood.objects.rank_food_by_calories()
        return results


class MacronutrientFoodDetail(RetrieveView, UpdateView, DestroyView):
    queryset = MacronutrientFood.objects.all()
    serializer_class = MacronutrientFoodSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = MacronutrientFoodSerializer(request.macronutrient_food)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = MacronutrientFoodSerializer(request.macronutrient_food, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        Food.objects.remove_macronutrient_from_food(request.macronutrient_food.food,
                                                    request.macronutrient_food.macronutrient)
        MacronutrientFood.objects.delete_macronutrient_food(request.macronutrient_food)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class MacronutrientFoodList(ListView, CreateView):
    serializer_class = MacronutrientFoodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        serializer = MacronutrientFoodSerializer(MacronutrientFood.objects.all(), many=True)
        return serializer.data

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = MacronutrientFoodSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
