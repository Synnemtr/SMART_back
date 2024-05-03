from django.urls import path
from api.food.views import (
    FoodList,
    FoodDetail,
    MacronutrientFoodList,
    MacronutrientFoodDetail,
    FoodIntakeList,
    FoodIntakeDetail,
    FoodTakenByUser,
    FoodTakenByUserDate,
    RankingFoodByCalories, 
    PlannedFoodList,
    PlannedFoodDetail,
    RankingFoodByUsers,
)

urlpatterns = [
    path("", FoodList.as_view({'get': 'list', 'post': 'create'})),
    path("ranking/", RankingFoodByCalories.as_view({'get': 'list'})),
    path("<int:pk>/", FoodDetail.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path("<int:food_id>/macronutrients/", MacronutrientFoodList.as_view({'get': 'list', 'post': 'create'})),
    path("<int:food_id>/macronutrients/<int:pk>/", MacronutrientFoodDetail.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path("food-intake/", FoodIntakeList.as_view({'get': 'list', 'post': 'create'})),
    path("food-intake/<int:pk>/", FoodIntakeDetail.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path("food-intake/user/", FoodTakenByUser.as_view({'get': 'list'})),
    path("food-intake/user/date/", FoodTakenByUserDate.as_view({'get': 'list'})),
    path("planned-food/", PlannedFoodList.as_view({'get': 'list', 'post': 'create'})),
    path("planned-food/<int:pk>/", PlannedFoodDetail.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path("ranking/food-by-users/", RankingFoodByUsers.as_view({'get': 'list'})),
]
